grammar Plexil;

//
// PARSER RULES
//

plexilPlan : declarations? action EOF ;

declarations : ( declaration SEMICOLON )+ ;

declaration :
    commandDeclaration
  | lookupDeclaration
  | libraryNodeDeclaration
  | mutexDeclaration
 ;

commandDeclaration :
    COMMAND_KYWD NCNAME paramsSpec?
  | returnType COMMAND_KYWD NCNAME paramsSpec?
  ;

lookupDeclaration : returnType LOOKUP_KYWD NCNAME paramsSpec? ;

paramsSpec : LPAREN paramsSpecGuts? RPAREN ;

paramsSpecGuts :
    paramSpec ( COMMA paramSpec )* ( COMMA ELLIPSIS )?
  | ELLIPSIS
 ;

paramSpec :
    baseTypeName LBRACKET INT RBRACKET
  | baseTypeName NCNAME LBRACKET INT RBRACKET
  | paramTypeName NCNAME?
 ;

paramTypeName : ANY_KYWD | baseTypeName ;

returnType : returnTypeSpec ;

returnTypeSpec :
    baseTypeName LBRACKET INT RBRACKET
  | baseTypeName
 ;

baseTypeName :
    BOOLEAN_KYWD
  | INTEGER_KYWD
  | REAL_KYWD
  | STRING_KYWD
  | DATE_KYWD
  | DURATION_KYWD
  ;

libraryNodeDeclaration :
    (LIBRARY_ACTION_KYWD | LIBRARY_NODE_KYWD) NCNAME libraryInterfaceSpec?
 ;

libraryInterfaceSpec :
    LPAREN ( libraryParamSpec ( COMMA libraryParamSpec )* )? RPAREN
 ;

libraryParamSpec :
    ( IN_KYWD | IN_OUT_KYWD ) baseTypeName ( NCNAME LBRACKET INT RBRACKET | NCNAME )
 ;

mutexDeclaration : MUTEX_KYWD NCNAME ( COMMA NCNAME )* ;

action : namedAction | baseAction ;

namedAction : actionId=NCNAME COLON rest=baseAction ;

baseAction : block | compoundAction | simpleStatement ;

compoundAction :
    ifAction
  | forAction
  | onCommandAction
  | onMessageAction
  | whileAction
 ;

simpleStatement : simpleAction SEMICOLON ;

simpleAction :
    assignment
  | commandInvocation
  | libraryCall
  | update
  | doAction
  | synchCmd
  | waitBuiltin
 ;

forAction :
    FOR_KYWD LPAREN baseTypeName NCNAME EQUALS loopvarinit=expression
    SEMICOLON endtest=expression SEMICOLON loopvarupdate=expression RPAREN
    action
 ;

ifAction :
    IF_KYWD expression consequentAction
    (ELSEIF_KYWD expression consequentAction)*
    (ELSE_KYWD action)?
    (ENDIF_KYWD SEMICOLON?)?
 ;

consequentAction : actionId=NCNAME COLON rest=consequent | consequent ;

consequent : block | compoundConsequent | simpleStatement ;

compoundConsequent : forAction | onCommandAction | onMessageAction | whileAction ;

onCommandAction :
    ON_COMMAND_KYWD expression (LPAREN parameterDeclaration (COMMA parameterDeclaration)* RPAREN)? action
 ;

parameterDeclaration :
    baseTypeName arrayVariableDecl
  | baseTypeName scalarVariableDecl
 ;

onMessageAction : ON_MESSAGE_KYWD expression action ;

whileAction : WHILE_KYWD expression action ;

doAction : DO_KYWD action WHILE_KYWD expression ;

synchCmd : SYNCHRONOUS_COMMAND_KYWD ( commandWithAssignment | commandInvocation ) synchCmdOptions? ;

synchCmdOptions : CHECKED_KYWD timeoutOption? | timeoutOption CHECKED_KYWD? ;

timeoutOption : TIMEOUT_KYWD expression ( COMMA expression )? ;

waitBuiltin : WAIT_KYWD expression (COMMA (variable|INT|DOUBLE))? ;

block :
    (sequenceVariantKywd LBRACE | LBRACE)
    comment?
    (nodeDeclaration SEMICOLON)*
    (nodeAttribute SEMICOLON)*
    action*
    RBRACE
    SEMICOLON?
 ;

sequenceVariantKywd :
    CONCURRENCE_KYWD | SEQUENCE_KYWD | CHECKED_SEQUENCE_KYWD
  | UNCHECKED_SEQUENCE_KYWD | TRY_KYWD
 ;

comment : COMMENT_KYWD STRING SEMICOLON ;

nodeDeclaration : interfaceDeclaration | variableDeclaration | mutexDeclaration ;

nodeAttribute : nodeCondition | mutexReference | priority | resource ;

nodeCondition : conditionKywd expression ;

conditionKywd :
    END_CONDITION_KYWD | EXIT_CONDITION_KYWD | INVARIANT_CONDITION_KYWD
  | POST_CONDITION_KYWD | PRE_CONDITION_KYWD | REPEAT_CONDITION_KYWD
  | SKIP_CONDITION_KYWD | START_CONDITION_KYWD
 ;

resource :
    RESOURCE_KYWD NAME_KYWD EQUALS expression
    ( COMMA ( UPPER_BOUND_KYWD EQUALS expression | RELEASE_AT_TERM_KYWD EQUALS expression ) )*
 ;

priority : PRIORITY_KYWD INT ;

interfaceDeclaration : in | inOut ;

in : IN_KYWD ( (NCNAME (COMMA NCNAME)*) | interfaceDeclarations ) ;

inOut : IN_OUT_KYWD ( (NCNAME (COMMA NCNAME)*) | interfaceDeclarations ) ;

interfaceDeclarations :
    baseTypeName ( arrayVariableDecl | scalarVariableDecl )
    ( COMMA ( arrayVariableDecl | scalarVariableDecl ) )*
 ;

variable : NCNAME ;

variableDeclaration :
    baseTypeName ( arrayVariableDecl | scalarVariableDecl )
    ( COMMA ( arrayVariableDecl | scalarVariableDecl ) )*
 ;

scalarVariableDecl : NCNAME ( EQUALS literalScalarValue )? ;

arrayVariableDecl : NCNAME LBRACKET INT RBRACKET ( EQUALS literalValue ) ? ;

literalValue : literalScalarValue | literalArrayValue ;

literalScalarValue : booleanLiteral | numericLiteral | STRING ;

numericLiteral : INT | DOUBLE | dateLiteral | durationLiteral | MINUS INT | MINUS DOUBLE ;

literalArrayValue : HASHPAREN literalScalarValue* RPAREN ;

booleanLiteral : TRUE_KYWD | FALSE_KYWD ;

mutexReference : USING_KYWD NCNAME ( COMMA NCNAME )* ;

lookupArrayReference : lookup LBRACKET expression RBRACKET ;

simpleArrayReference : variable LBRACKET expression RBRACKET ;

commandInvocation :
    ( NCNAME | LPAREN expression RPAREN ) LPAREN argumentList? RPAREN
 ;

commandWithAssignment : assignmentLHS EQUALS commandInvocation ;

argumentList : argument (COMMA argument)* ;

argument : expression ;

assignment : assignmentLHS EQUALS assignmentRHS ;

assignmentLHS : simpleArrayReference | variable ;

assignmentRHS : commandInvocation | expression ;

update : UPDATE_KYWD ( pair ( COMMA pair )* )? ;

pair : NCNAME EQUALS expression ;

libraryCall : LIBRARY_CALL_KYWD NCNAME ( LPAREN ( aliasSpec ( COMMA aliasSpec )* ) ? RPAREN )? ;

aliasSpec : NCNAME EQUALS expression ;

nodeParameterName : NCNAME ;


// Expressions
expression : logicalOr ;

logicalOr : logicalXOR ( OR_KYWD logicalXOR )* ;

logicalXOR : logicalAnd ( XOR_KYWD logicalAnd )* ;

logicalAnd : equality ( AND_KYWD equality )* ;

equality : relational ( equalityOp relational )? ;

equalityOp : DEQUALS | NEQUALS ;

relational : additive ( relationalOp additive )? ;

relationalOp : GREATER | GEQ | LESS | LEQ ;

additive : multiplicative ( addOp multiplicative )* ;

addOp : PLUS | MINUS ;

multiplicative : unary ( multOp unary )* ;

multOp : ASTERISK | SLASH | PERCENT | MOD_KYWD ;

unary : unaryMinus | unaryOp logicalQuantity | quantity ;

unaryOp : NOT_KYWD ;

unaryMinus : MINUS INT | MINUS DOUBLE | MINUS numericQuantity ;

dateLiteral : DATE_KYWD LPAREN STRING RPAREN ;

durationLiteral : DURATION_KYWD LPAREN STRING RPAREN ;

numericQuantity :
    LPAREN expression RPAREN
  | BAR expression BAR
  | oneArgNumericFn LPAREN expression RPAREN
  | twoArgNumericFn LPAREN expression COMMA expression RPAREN
  | lookupArrayReference
  | lookupExpr
  | nodeTimepointValue
  | variable
  | numericLiteral
 ;

logicalQuantity :
    LPAREN expression RPAREN
  | isKnownExp
  | lookupArrayReference
  | lookupExpr
  | messageReceivedExp
  | nodeStatePredicateExp
  | simpleArrayReference
  | variable
  | booleanLiteral
 ;

quantity :
    LPAREN expression RPAREN
  | BAR expression BAR
  | oneArgNumericFn LPAREN expression RPAREN
  | twoArgNumericFn LPAREN expression COMMA expression RPAREN
  | isKnownExp
  | lookupArrayReference
  | lookupExpr
  | messageReceivedExp
  | nodeStatePredicateExp
  | simpleArrayReference
  | nodeCommandHandleVariable
  | nodeFailureVariable
  | nodeOutcomeVariable
  | nodeStateVariable
  | nodeTimepointValue
  | variable
  | literalValue
  | nodeCommandHandleLiteral
  | nodeFailureLiteral
  | nodeStateLiteral
  | nodeOutcomeLiteral
 ;

oneArgNumericFn :
    SQRT_KYWD | ABS_KYWD | CEIL_KYWD | FLOOR_KYWD
  | ROUND_KYWD | TRUNC_KYWD | REAL_TO_INT_KYWD
  | STRLEN_KYWD | ARRAY_SIZE_KYWD | ARRAY_MAX_SIZE_KYWD
 ;

twoArgNumericFn : MAX_KYWD | MIN_KYWD ;

isKnownExp : IS_KNOWN_KYWD LPAREN quantity RPAREN ;

nodeStatePredicate :
    NODE_EXECUTING_KYWD | NODE_FAILED_KYWD | NODE_FINISHED_KYWD
  | NODE_INACTIVE_KYWD | NODE_INVARIANT_FAILED_KYWD
  | NODE_ITERATION_ENDED_KYWD | NODE_ITERATION_FAILED_KYWD
  | NODE_ITERATION_SUCCEEDED_KYWD | NODE_PARENT_FAILED_KYWD
  | NODE_POSTCONDITION_FAILED_KYWD | NODE_PRECONDITION_FAILED_KYWD
  | NODE_SKIPPED_KYWD | NODE_SUCCEEDED_KYWD | NODE_WAITING_KYWD
  | NO_CHILD_FAILED_KYWD
 ;

nodeStatePredicateExp : nodeStatePredicate LPAREN nodeReference RPAREN ;

nodeStateLiteral :
    EXECUTING_STATE_KYWD | FAILING_STATE_KYWD | FINISHED_STATE_KYWD
  | FINISHING_STATE_KYWD | INACTIVE_STATE_KYWD | ITERATION_ENDED_STATE_KYWD
  | WAITING_STATE_KYWD
 ;

messageReceivedExp : MESSAGE_RECEIVED_KYWD LPAREN STRING RPAREN ;

nodeState : nodeStateVariable | nodeStateLiteral ;

nodeStateVariable : nodeReference PERIOD STATE_KYWD ;

nodeOutcome : nodeOutcomeVariable | nodeOutcomeLiteral ;

nodeOutcomeVariable : nodeReference PERIOD OUTCOME_KYWD ;

nodeOutcomeLiteral :
    SUCCESS_OUTCOME_KYWD | FAILURE_OUTCOME_KYWD
  | SKIPPED_OUTCOME_KYWD | INTERRUPTED_OUTCOME_KYWD
 ;

nodeCommandHandle : nodeCommandHandleVariable | nodeCommandHandleLiteral ;

nodeCommandHandleVariable : nodeReference PERIOD COMMAND_HANDLE_KYWD ;

nodeCommandHandleLiteral :
    COMMAND_ABORTED_KYWD | COMMAND_ABORT_FAILED_KYWD
  | COMMAND_ACCEPTED_KYWD | COMMAND_DENIED_KYWD
  | COMMAND_FAILED_KYWD | COMMAND_INTERFACE_ERROR_KYWD
  | COMMAND_RCVD_KYWD | COMMAND_SENT_KYWD | COMMAND_SUCCESS_KYWD
 ;

nodeFailure : nodeFailureVariable | nodeFailureLiteral ;

nodeFailureVariable : nodeReference PERIOD FAILURE_KYWD ;

nodeFailureLiteral :
    PRE_CONDITION_FAILED_KYWD | POST_CONDITION_FAILED_KYWD
  | INVARIANT_CONDITION_FAILED_KYWD | PARENT_FAILED_KYWD
  | PARENT_EXITED_KYWD | EXITED_KYWD
 ;

nodeTimepointValue : nodeReference PERIOD nodeStateLiteral PERIOD timepoint ;

timepoint : START_KYWD | END_KYWD ;

nodeReference : NCNAME | nodeRef ;

nodeRef :
    SELF_KYWD | PARENT_KYWD
  | CHILD_KYWD LPAREN NCNAME RPAREN
  | SIBLING_KYWD LPAREN NCNAME RPAREN
 ;

lookupExpr : lookupOnChange | lookupNow | lookup ;

lookupOnChange : LOOKUP_ON_CHANGE_KYWD LPAREN lookupInvocation (COMMA expression)? RPAREN ;

lookupNow : LOOKUP_NOW_KYWD LPAREN lookupInvocation RPAREN ;

lookup : LOOKUP_KYWD LPAREN lookupInvocation (COMMA expression)? RPAREN ;

lookupInvocation : ( stateName | ( LPAREN stateNameExp RPAREN ) ) ( LPAREN argumentList? RPAREN )? ;

stateName : NCNAME ;

stateNameExp : expression ;


//
// LEXER RULES
//

// Keywords
COMMENT_KYWD : 'Comment';
COMMAND_KYWD : 'Command';
LOOKUP_KYWD  : 'Lookup';
MUTEX_KYWD   : 'Mutex';
RETURNS_KYWD : 'Returns';
RESOURCE_KYWD: 'Resource';
NAME_KYWD    : 'Name';
UPPER_BOUND_KYWD : 'UpperBound';
RELEASE_AT_TERM_KYWD : 'ReleaseAtTermination';
PRIORITY_KYWD : 'Priority';
USING_KYWD : 'Using';
IN_KYWD : 'In';
IN_OUT_KYWD : 'InOut';
ANY_KYWD : 'Any';
BOOLEAN_KYWD : 'Boolean';
INTEGER_KYWD : 'Integer';
REAL_KYWD : 'Real';
STRING_KYWD : 'String';
DATE_KYWD : 'Date';
DURATION_KYWD : 'Duration';
UPDATE_KYWD : 'Update';
LIBRARY_CALL_KYWD : 'LibraryCall';
LIBRARY_ACTION_KYWD : 'LibraryAction';
LIBRARY_NODE_KYWD : 'LibraryNode';
STATE_KYWD : 'state';
OUTCOME_KYWD : 'outcome';
COMMAND_HANDLE_KYWD : 'command_handle';
FAILURE_KYWD : 'failure';
WAITING_STATE_KYWD : 'WAITING';
EXECUTING_STATE_KYWD : 'EXECUTING';
FINISHING_STATE_KYWD : 'FINISHING';
FAILING_STATE_KYWD : 'FAILING';
FINISHED_STATE_KYWD : 'FINISHED';
ITERATION_ENDED_STATE_KYWD : 'ITERATION_ENDED';
INACTIVE_STATE_KYWD : 'INACTIVE';
SUCCESS_OUTCOME_KYWD : 'SUCCESS';
FAILURE_OUTCOME_KYWD : 'FAILURE';
SKIPPED_OUTCOME_KYWD : 'SKIPPED';
INTERRUPTED_OUTCOME_KYWD : 'INTERRUPTED';
COMMAND_ABORTED_KYWD : 'COMMAND_ABORTED';
COMMAND_ABORT_FAILED_KYWD : 'COMMAND_ABORT_FAILED';
COMMAND_ACCEPTED_KYWD : 'COMMAND_ACCEPTED';
COMMAND_DENIED_KYWD : 'COMMAND_DENIED';
COMMAND_FAILED_KYWD : 'COMMAND_FAILED';
COMMAND_INTERFACE_ERROR_KYWD : 'COMMAND_INTERFACE_ERROR';
COMMAND_RCVD_KYWD : 'COMMAND_RCVD_BY_SYSTEM';
COMMAND_SENT_KYWD : 'COMMAND_SENT_TO_SYSTEM';
COMMAND_SUCCESS_KYWD : 'COMMAND_SUCCESS';
PRE_CONDITION_FAILED_KYWD : 'PRE_CONDITION_FAILED';
POST_CONDITION_FAILED_KYWD : 'POST_CONDITION_FAILED';
INVARIANT_CONDITION_FAILED_KYWD : 'INVARIANT_CONDITION_FAILED';
PARENT_FAILED_KYWD : 'PARENT_FAILED';
PARENT_EXITED_KYWD : 'PARENT_EXITED';
EXITED_KYWD : 'EXITED';
TRUE_KYWD : 'true';
FALSE_KYWD : 'false';
START_KYWD : 'START';
END_KYWD : 'END';
LOOKUP_ON_CHANGE_KYWD : 'LookupOnChange';
LOOKUP_NOW_KYWD : 'LookupNow';
XOR_KYWD : 'XOR';
ABS_KYWD : 'abs';
IS_KNOWN_KYWD : 'isKnown';
SQRT_KYWD : 'sqrt';
MAX_KYWD : 'max';
MIN_KYWD : 'min';
MOD_KYWD : 'mod';
CEIL_KYWD : 'ceil';
FLOOR_KYWD : 'floor';
ROUND_KYWD : 'round';
TRUNC_KYWD : 'trunc';
REAL_TO_INT_KYWD : 'real_to_int';
STRLEN_KYWD : 'strlen';
ARRAY_SIZE_KYWD : 'arraySize';
ARRAY_MAX_SIZE_KYWD : 'arrayMaxSize';
CHILD_KYWD : 'Child';
PARENT_KYWD : 'Parent';
SELF_KYWD : 'Self';
SIBLING_KYWD : 'Sibling';
NODE_EXECUTING_KYWD : 'NodeExecuting';
NODE_FAILED_KYWD : 'NodeFailed';
NODE_FINISHED_KYWD : 'NodeFinished';
NODE_INACTIVE_KYWD : 'NodeInactive';
NODE_INVARIANT_FAILED_KYWD : 'NodeInvariantFailed';
NODE_ITERATION_ENDED_KYWD : 'NodeIterationEnded';
NODE_ITERATION_FAILED_KYWD : 'NodeIterationFailed';
NODE_ITERATION_SUCCEEDED_KYWD : 'NodeIterationSucceeded';
NODE_PARENT_FAILED_KYWD : 'NodeParentFailed';
NODE_POSTCONDITION_FAILED_KYWD : 'NodePostconditionFailed';
NODE_PRECONDITION_FAILED_KYWD : 'NodePreconditionFailed';
NODE_SKIPPED_KYWD : 'NodeSkipped';
NODE_SUCCEEDED_KYWD : 'NodeSucceeded';
NODE_WAITING_KYWD : 'NodeWaiting';
NO_CHILD_FAILED_KYWD : 'NoChildFailed';
CONCURRENCE_KYWD : 'Concurrence';
ON_COMMAND_KYWD : 'OnCommand';
ON_MESSAGE_KYWD : 'OnMessage';
SYNCHRONOUS_COMMAND_KYWD : 'SynchronousCommand';
TIMEOUT_KYWD : 'Timeout';
CHECKED_KYWD : 'Checked';
TRY_KYWD : 'Try';
UNCHECKED_SEQUENCE_KYWD : 'UncheckedSequence';
CHECKED_SEQUENCE_KYWD : 'CheckedSequence';
SEQUENCE_KYWD : 'Sequence';
WAIT_KYWD : 'Wait';
DO_KYWD : 'do';
ELSE_KYWD : 'else';
ELSEIF_KYWD : 'elseif';
ENDIF_KYWD : 'endif';
FOR_KYWD : 'for';
IF_KYWD : 'if';
WHILE_KYWD : 'while';
MESSAGE_RECEIVED_KYWD : 'MessageReceived';

START_CONDITION_KYWD : 'StartCondition' | 'Start' ;
REPEAT_CONDITION_KYWD : 'RepeatCondition' | 'Repeat' ;
SKIP_CONDITION_KYWD : 'SkipCondition' | 'Skip' ;
PRE_CONDITION_KYWD : 'PreCondition' | 'Pre' ;
POST_CONDITION_KYWD : 'PostCondition' | 'Post';
INVARIANT_CONDITION_KYWD : 'InvariantCondition' | 'Invariant';
END_CONDITION_KYWD : 'EndCondition' | 'End' ;
EXIT_CONDITION_KYWD : 'ExitCondition' | 'Exit' ;

AND_KYWD : 'AND' | '&&' ;
OR_KYWD : 'OR' | '||' ;
NOT_KYWD : 'NOT' | '!' ;

// Operators and Punctuation
LBRACKET : '[';
RBRACKET : ']';
LBRACE : '{';
RBRACE : '}';
LPAREN : '(';
RPAREN : ')';
BAR : '|';
LESS : '<' ;
GREATER : '>' ;
LEQ : '<=' ;
GEQ : '>=' ;
COLON : ':';
DEQUALS : '==';
NEQUALS : '!=';
EQUALS : '=';
ASTERISK : '*';
SLASH : '/';
PERCENT : '%';
HASHPAREN : '#(';
ELLIPSIS : '...';
SEMICOLON : ';';
COMMA : ',';
PLUS : '+';
MINUS : '-';
PERIOD : '.';

// Literals and Data Types
STRING: '"' (Escape|~('"'|'\\'))* '"'
      | '\'' (Escape|~('\''|'\\'))* '\''
      ;

DOUBLE :
    Digit+ PERIOD Digit* Exponent?
  | PERIOD Digit+ Exponent?
  | Digit+ Exponent
  ;

INT :
    '0' ('x'|'X') HexDigit+
  | '0' ('o'|'O') OctalDigit+
  | '0' ('b'|'B') ('0'|'1')+
  | Digit+
  ;

NCNAME : (Letter|'_') (Letter|Digit|'_')* ;

WS : ( ' ' | '\t' | '\f' | '\n' | '\r' )+ -> channel(HIDDEN) ;

SL_COMMENT :
    ( '//' ~('\r' | '\n')* ('\r\n' | '\r' | '\n')
    | '//' ~('\r' | '\n')*
    ) -> channel(HIDDEN)
 ;

ML_COMMENT : '/*' .*? '*/' -> channel(HIDDEN) ;

// Fragments
fragment Escape : '\\' ('b' | 'f' | 'n' | 't' | '\n' | '\r' | '"' | '\'' | '\\' | UnicodeEscape | UnicodeLongEscape | HexEscape | OctalEscape) ;
fragment UnicodeEscape: 'u' HexDigit HexDigit HexDigit HexDigit;
fragment UnicodeLongEscape: 'U' HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit;
fragment HexEscape: 'x' HexDigit+ ;
fragment OctalEscape: ('0'..'3') ( OctalDigit OctalDigit? )? | ('4'..'7') OctalDigit? ;
fragment OctalDigit: ('0'..'7') ;
fragment Digit: ('0'..'9') ;
fragment HexDigit: (Digit|'A'..'F'|'a'..'f') ;
fragment Exponent: ('e'|'E') (PLUS | MINUS)? Digit+ ;
fragment Letter : 'a'..'z'|'A'..'Z' ;