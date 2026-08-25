// PlexilScript.g4
grammar PlexilScript;

// ---------------------------------------------------------
// PARSER RULES
// ---------------------------------------------------------

plexilScript : elements EOF ;

elements : element* ;

element : initialState
        | script
        | stateDef
        | updateAck
        | command
        | functionCall
        | commandAbort
        | simultaneous
        | commandAck
        | commandAccepted
        | commandDenied
        | commandSentToSystem
        | commandRcvdBySystem
        | commandSuccess
        | commandFailed
        | delay
        ;

initialState : 'initial-state' LBRACE elements RBRACE ;

simultaneous : 'simultaneous' LBRACE elements RBRACE ;

script : 'script' LBRACE elements RBRACE ;

updateAck : 'update-ack' ID SEMI ;

stateDef : 'state' ID parameters EQUALS values COLON type SEMI ;

functionCall : 'function-call' ID parameters EQUALS results COLON type SEMI ;

command : 'command' ID parameters EQUALS results COLON type SEMI ;

commandAbort : 'command-abort' ID parameters EQUALS results COLON type SEMI ;

commandAck : 'command-ack' ID parameters EQUALS results COLON type SEMI ;

commandAccepted : 'command-accepted' ID parameters SEMI ;

commandDenied : 'command-denied' ID parameters SEMI ;

commandSentToSystem : 'command-sent-to-system' ID parameters SEMI ;

commandRcvdBySystem : 'command-rcvd-by-system' ID parameters SEMI ;

commandSuccess : 'command-success' ID parameters SEMI ;

commandFailed : 'command-failed' ID parameters SEMI ;

delay : 'delay' SEMI ;

parameters : LPAREN (parameter (COMMA parameter)*)? RPAREN ;

parameter : value COLON type ;

values : value
       | LPAREN value (COMMA value)* RPAREN
       ;

results : value
        | LPAREN value (COMMA value)* RPAREN
        ;

value : 'true'
      | 'false'
      | UNKNOWN
      | STRING
      | NUMBER
      ;

type : 'int-array'
     | 'string-array'
     | 'real-array'
     | 'string'
     | 'bool-array'
     | 'int'
     | 'real'
     | 'bool'
     ;

// ---------------------------------------------------------
// LEXER RULES
// ---------------------------------------------------------

LBRACE : '{';
RBRACE : '}';
LPAREN : '(';
RPAREN : ')';
SEMI   : ';';
COMMA  : ',';
COLON  : ':';
EQUALS : '=';

UNKNOWN : '<unknown>' ;
STRING  : '"' ~'"'* '"' ;
NUMBER  : '-'? DIGIT+ ('.' DIGIT+)? ;
ID      : LETTER (LETTER | DIGIT | '_' | '-' | '.')* ;

WS      : [ \t\r\n]+ -> skip ;
COMMENT : '//' ~[\r\n]* -> skip ;

fragment LETTER : [a-zA-Z] ;
fragment DIGIT  : [0-9] ;