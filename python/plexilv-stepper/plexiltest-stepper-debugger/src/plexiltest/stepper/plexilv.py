import maude
from pathlib import Path

from ..shared import StepperInterpreter

class PLEXILVTest(StepperInterpreter):

    def __init__(self,*, plexilv_home, script, plan):
        self.plexilv_home = Path(plexilv_home)
        self.script = Path(script)
        self.plan = Path(plan)

        if not self.plexilv_home.is_dir():
            raise NotADirectoryError(f"PLEXILV home directory not found: {self.plexilv_home}")
        if not self.script.is_file():
            raise FileNotFoundError(f"Script file not found: {self.script}")
        if not self.plan.is_file():
            raise FileNotFoundError(f"Plan file not found: {self.plan}")

        framework_module = self.plexilv_home / "semantics" / "src" / "plexil-v.maude"
        if not framework_module.is_file():
            raise FileNotFoundError(f"PLEXIL-V framework module not found: {framework_module}")

        maude.init()
        maude.load(str(framework_module))
        maude.load(str(self.script))
        maude.load(str(self.plan))

        plan_name = self.plan.stem
        module_text = f"""
        mod PLAN-SIMULATION is
            protecting {plan_name}-PLAN .
            protecting INPUT .
        endm
        """
        maude.input(module_text)

        mod = maude.getModule("PLAN-SIMULATION")
        if mod is None:
            raise ValueError("Failed to create and get the module 'PLAN-SIMULATION'.")

        self.term = mod.parseTerm("run(compile(rootNode,input))")
        if self.term is None:
            raise ValueError("Failed to parse the term 'run(compile(rootNode,input))' from the current Maude module.")

        try:
            self.term.reduce()
        except Exception as e:
            raise RuntimeError(f"Failed to reduce the term: {e}")

    def needs_step(self) -> bool:
        term_copy = self.term.copy()
        num_rewrites = term_copy.rewrite(1)
        return num_rewrites > 0 and term_copy != self.term

    def step(self) -> None:
        self.term.rewrite(1)

    def _term_to_clean_str(self, term) -> str:
        try:
            term_args = list(term.arguments())
            if term_args:
                return term.prettyPrint(0)

            sort_name = str(term.getSort())
            if sort_name == 'Qid':
                return term.prettyPrint(0)

            return str(term.symbol())
        except:
            return term.prettyPrint(0)

    def _extract_nodes(self, term_str: str) -> dict:
        mod = maude.getModule("PLAN-SIMULATION")
        nodes_dict = {}
        nodes_term = mod.parseTerm(f"getNodes(({term_str}))")
        if nodes_term is not None:
            nodes_term.reduce()

            def process_term(t):
                if t.isVariable():
                    return

                # Check for constant by checking arguments
                try:
                    args = list(t.arguments())
                except:
                    return

                if not args:
                    return

                sym = t.symbol()
                if sym is not None and str(sym) == '<_:_|_>':
                    args = list(t.arguments())
                    if len(args) >= 3:
                        oid_term = args[0]
                        oid_str = oid_term.prettyPrint(maude.PRINT_MIXFIX)
                        if oid_str.startswith('"') and oid_str.endswith('"'):
                            oid_str = oid_str[1:-1]

                        attrs = args[2]
                        status = "UNKNOWN"
                        outcome = "UNKNOWN"

                        def extract_attrs(at):
                            if at.isVariable():
                                return

                            try:
                                at_args = list(at.arguments())
                            except:
                                return

                            if not at_args:
                                return

                            at_sym = at.symbol()
                            if at_sym is not None:
                                if str(at_sym) == 'status:_':
                                    status_args = list(at.arguments())
                                    if status_args:
                                        nonlocal status
                                        status = self._term_to_clean_str(status_args[0])
                                elif str(at_sym) == 'outcome:_':
                                    outcome_args = list(at.arguments())
                                    if outcome_args:
                                        nonlocal outcome
                                        outcome = self._term_to_clean_str(outcome_args[0])
                                else:
                                    for a in at.arguments():
                                        extract_attrs(a)

                        extract_attrs(attrs)
                        nodes_dict[oid_str] = {"status": status, "outcome": outcome}
                else:
                    for arg in t.arguments():
                        process_term(arg)

            process_term(nodes_term)
        return nodes_dict

    def _parse_generator_set(self, term) -> list:
        sym = term.symbol()
        sym_str = str(sym) if sym is not None else ""
        if sym_str == 'noInputs':
            return []
        if sym_str == '__':
            try:
                res = []
                for arg in term.arguments():
                    res.extend(self._parse_generator_set(arg))
                return res
            except:
                return []

        # Base case: single input element
        return [term.prettyPrint(maude.PRINT_MIXFIX)]

    def _parse_generator_list(self, term) -> list:
        sym = term.symbol()
        sym_str = str(sym) if sym is not None else ""
        if sym_str == 'nilEInputsList':
            return []
        if sym_str == '_#_':
            try:
                res = []
                for arg in term.arguments():
                    res.extend(self._parse_generator_list(arg))
                return res
            except:
                return []

        # Base case: single set element
        return [self._parse_generator_set(term)]

    def _extract_generator_raw(self, term_str: str) -> str:
        mod = maude.getModule("PLAN-SIMULATION")
        gen_term = mod.parseTerm(f"getEnvironmentGenerator(({term_str}))")

        if gen_term is not None:
            gen_term.reduce()
            sym = gen_term.symbol()
            if sym is None or str(sym) != 'sequenceGenerator':
                raise ValueError("only the sequenceGenerator is supported by the stepper")

            args = list(gen_term.arguments())
            if not args:
                raise ValueError("sequenceGenerator has no arguments")

            return args[0].prettyPrint(maude.PRINT_MIXFIX)

        raise ValueError("Error: Could not parse generator term")

    def _extract_generator(self, term_str: str) -> list:
        mod = maude.getModule("PLAN-SIMULATION")
        gen_term = mod.parseTerm(f"getEnvironmentGenerator(({term_str}))")

        if gen_term is not None:
            gen_term.reduce()
            sym = gen_term.symbol()
            if sym is None or str(sym) != 'sequenceGenerator':
                raise ValueError("only the sequenceGenerator is supported by the stepper")

            args = list(gen_term.arguments())
            if not args:
                raise ValueError("sequenceGenerator has no arguments")

            return self._parse_generator_list(args[0])

        raise ValueError("Error: Could not parse generator term")

    def _extract_variables(self, term_str: str) -> dict:
        mod = maude.getModule("PLAN-SIMULATION")
        vars_dict = {}
        vars_term = mod.parseTerm(f"getVariables(({term_str}))")

        if vars_term is not None:
            vars_term.reduce()

            def process_term(t):
                if t.isVariable():
                    return

                try:
                    args = list(t.arguments())
                except:
                    return

                if not args:
                    return

                sym = t.symbol()
                if sym is not None and str(sym) == '<_:_|_>':
                    args = list(t.arguments())
                    if len(args) >= 3:
                        cid_term = args[1]
                        if str(cid_term.symbol()) == 'memory':
                            oid_term = args[0]
                            oid_str = oid_term.prettyPrint(maude.PRINT_MIXFIX)

                            # Clean quotes from string bounds if present
                            if oid_str.startswith('"') and oid_str.endswith('"'):
                                oid_str = oid_str[1:-1]

                            # Oid format: 'VarName . 'NodeB . 'NodeA
                            split_oid = oid_str.split(' . ')
                            if len(split_oid) >= 2:
                                var_name = split_oid[0]
                                node_id = ' . '.join(split_oid[1:])

                                attrs = args[2]
                                value = "UNKNOWN"

                                def extract_attrs(at):
                                    if at.isVariable():
                                        return
                                    try:
                                        at_args = list(at.arguments())
                                    except:
                                        return
                                    if not at_args:
                                        return

                                    at_sym = at.symbol()
                                    if at_sym is not None:
                                        if str(at_sym) == 'actVal:_':
                                            val_args = list(at.arguments())
                                            if val_args:
                                                nonlocal value
                                                value = self._term_to_clean_str(val_args[0])
                                        else:
                                            for a in at.arguments():
                                                extract_attrs(a)

                                extract_attrs(attrs)

                                if node_id not in vars_dict:
                                    vars_dict[node_id] = {}
                                vars_dict[node_id][var_name] = value
                else:
                    for arg in t.arguments():
                        process_term(arg)

            process_term(vars_term)
        return vars_dict

    def _parse_environment_set(self, term) -> list:
        sym = term.symbol()
        sym_str = str(sym) if sym is not None else ""
        if sym_str == 'mtenvironment':
            return []
        if sym_str == '_`,_':
            try:
                res = []
                for arg in term.arguments():
                    res.extend(self._parse_environment_set(arg))
                return res
            except:
                return []
        if sym_str == '_`(_`):_':
            try:
                args = list(term.arguments())
                if len(args) >= 3:
                    qid = self._term_to_clean_str(args[0])
                    if qid.startswith("'"):
                        qid = qid[1:]
                    env_args = self._term_to_clean_str(args[1])
                    val = self._term_to_clean_str(args[2])
                    return [{"name": qid, "args": env_args, "value": val}]
            except:
                pass
        return []

    def _extract_environment(self, term_str: str) -> list:
        mod = maude.getModule("PLAN-SIMULATION")
        env_term = mod.parseTerm(f"getEnvironment(({term_str}))")

        if env_term is not None:
            env_term.reduce()
            return self._parse_environment_set(env_term)
        return []

    def get_current_state(self) -> dict:
        term_str = self.term.prettyPrint(0)

        nodes = self._extract_nodes(term_str)
        vars_by_node = self._extract_variables(term_str)
        environment = self._extract_environment(term_str)

        for node_id, node_data in nodes.items():
            node_data["variables"] = vars_by_node.get(node_id, {})

        return {
            # "state": self.term.prettyPrint(maude.PRINT_FORMAT),
            # "generator_raw": self._extract_generator_raw(term_str),
            "generator": self._extract_generator(term_str),
            "nodes": nodes,
            "environment": environment
        }
