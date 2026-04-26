// Grammar file for Infrastructure DSL
// ANTLR version 4
// This grammar defines the complete syntax for the Infrastructure Modeling DSL

grammar InfrastructureDSL;

// Parser Rules (Production Rules)

// ============ Program Structure ============
program
    : compilationUnit* EOF
    ;

compilationUnit
    : statement
    | functionDeclaration
    | moduleDeclaration
    | variableDeclaration
    | constantDeclaration
    | roleDeclaration
    | policyDeclaration
    | assignment
    | useStatement
    | connectStatement
    | attachStatement
    | assignStatement
    | ifStatement
    | forStatement
    | comment
    ;

// ============ Statements ============
statement
    : resourceDeclaration
    | networkDeclaration
    | databaseDeclaration
    | securityGroupDeclaration
    | loadBalancerDeclaration
    | cacheDeclaration
    | containerDeclaration
    | functionResourceDeclaration
    | subnetDeclaration
    ;

// ============ Resource Declarations ============
resourceDeclaration
    : 'server' identifier resourceBlock
    ;

networkDeclaration
    : 'network' identifier resourceBlock
    ;

databaseDeclaration
    : 'database' identifier resourceBlock
    | 'nosql_db' identifier resourceBlock
    ;

securityGroupDeclaration
    : 'security_group' identifier resourceBlock
    ;

loadBalancerDeclaration
    : 'load_balancer' identifier resourceBlock
    ;

cacheDeclaration
    : 'cache' identifier resourceBlock
    ;

containerDeclaration
    : 'container' identifier resourceBlock
    ;

functionResourceDeclaration
    : 'function' identifier resourceBlock
    ;

subnetDeclaration
    : 'subnet' identifier resourceBlock
    ;

// ============ Resource Block ============
resourceBlock
    : '{' attributeList? '}'
    ;

attributeList
    : attribute (',' attribute)*
    ;

attribute
    : identifier '=' expression
    | identifier '=' objectLiteral
    | identifier '=' arrayLiteral
    | identifier '=' conditionalExpression
    ;

// ============ Expressions ============
expression
    : literal
    | identifier
    | functionCall
    | memberAccess
    | arrayAccess
    | '(' expression ')'
    | expression binaryOperator expression
    | expression 'and' expression
    | expression 'or' expression
    | 'not' expression
    | '-' expression
    | '+' expression
    ;

binaryOperator
    : '+' | '-' | '*' | '/' | '%' | '**'
    | '==' | '!=' | '<' | '<=' | '>' | '>='
    | 'in' | 'not' 'in'
    ;

conditionalExpression
    : 'if' conditionalClause 'then' expression ('else' expression)?
    ;

conditionalClause
    : expression
    ;

// ============ Function Declarations ============
functionDeclaration
    : 'function' identifier '(' parameterList? ')' functionBody
    ;

parameterList
    : parameter (',' parameter)*
    ;

parameter
    : identifier
    ;

functionBody
    : '{' statementList? 'return' expression ';' '}'
    ;

functionCall
    : identifier '(' argumentList? ')'
    ;

argumentList
    : expression (',' expression)*
    ;

// ============ Module Declarations ============
moduleDeclaration
    : 'module' identifier moduleBody
    ;

moduleBody
    : '{' moduleParameterList? moduleStatementList? '}'
    ;

moduleParameterList
    : moduleParameter (',' moduleParameter)*
    ;

moduleParameter
    : 'param' identifier '=' expression
    ;

moduleStatementList
    : moduleStatement+
    ;

moduleStatement
    : statement
    | forStatement
    | ifStatement
    | assignment
    | comment
    ;

// ============ Variable and Constant Declarations ============
variableDeclaration
    : 'variable' identifier variableBlock
    ;

constantDeclaration
    : 'constant' identifier '=' expression
    ;

variableBlock
    : '{' variableAttributeList? '}'
    ;

variableAttributeList
    : variableAttribute (',' variableAttribute)*
    ;

variableAttribute
    : 'type' '=' stringLiteral
    | 'default' '=' expression
    | 'description' '=' stringLiteral
    ;

// ============ Role Declarations ============
roleDeclaration
    : 'role' identifier roleBlock
    ;

roleBlock
    : '{' roleAttributeList? '}'
    ;

roleAttributeList
    : roleAttribute (',' roleAttribute)*
    ;

roleAttribute
    : 'description' '=' stringLiteral
    | 'permissions' '=' arrayLiteral
    | 'resources' '=' arrayLiteral
    | 'conditions' '=' objectLiteral
    ;

// ============ Policy Declarations ============
policyDeclaration
    : 'policy' identifier policyBlock
    ;

policyBlock
    : '{' policyAttributeList? '}'
    ;

policyAttributeList
    : policyAttribute (',' policyAttribute)*
    ;

policyAttribute
    : 'target' '=' expression
    | 'type' '=' stringLiteral
    | 'min_instances' '=' integerLiteral
    | 'max_instances' '=' integerLiteral
    | 'desired_capacity' '=' integerLiteral
    | 'rules' '=' arrayLiteral
    | 'metrics' '=' arrayLiteral
    | 'alarms' '=' arrayLiteral
    | 'schedule' '=' stringLiteral
    | 'retention_days' '=' integerLiteral
    | 'backup_retention' '=' integerLiteral
    | 'scale_up_cooldown' '=' integerLiteral
    | 'scale_down_cooldown' '=' integerLiteral
    | 'log_groups' '=' arrayLiteral
    | 'log_streams' '=' arrayLiteral
    ;

// ============ Control Flow Statements ============
ifStatement
    : 'if' expression block ('else' block)?
    ;

forStatement
    : 'for' identifier 'in' expression block
    ;

block
    : '{' statementList? '}'
    ;

statementList
    : statement+
    ;

// ============ Assignment Statements ============
assignment
    : identifier '=' expression
    ;

// ============ Use Statement ============
useStatement
    : 'use' identifier 'with' objectLiteral
    ;

// ============ Connect Statement ============
connectStatement
    : 'connect' expression '->' expression connectionBlock
    ;

connectionBlock
    : '{' connectionAttributeList? '}'
    ;

connectionAttributeList
    : connectionAttribute (',' connectionAttribute)*
    ;

connectionAttribute
    : identifier '=' expression
    ;

// ============ Attach Statement ============
attachStatement
    : 'attach' expression 'to' expression
    ;

// ============ Assign Statement ============
assignStatement
    : 'assign' identifier 'to' userSpecification
    ;

userSpecification
    : 'user' stringLiteral
    | 'group' stringLiteral
    | 'role' stringLiteral
    ;

// ============ Literals ============
literal
    : integerLiteral
    | floatLiteral
    | stringLiteral
    | booleanLiteral
    | sizeLiteral
    | nullLiteral
    ;

integerLiteral
    : INTEGER
    ;

floatLiteral
    : FLOAT
    ;

stringLiteral
    : STRING
    ;

booleanLiteral
    : 'true' | 'false'
    ;

sizeLiteral
    : SIZE
    ;

nullLiteral
    : 'null'
    ;

// ============ Complex Literals ============
objectLiteral
    : '{' objectPropertyList? '}'
    ;

objectPropertyList
    : objectProperty (',' objectProperty)*
    ;

objectProperty
    : identifier ':' expression
    | stringLiteral ':' expression
    ;

arrayLiteral
    : '[' expressionList? ']'
    ;

expressionList
    : expression (',' expression)*
    ;

// ============ Member Access ============
memberAccess
    : expression '.' identifier
    ;

// ============ Array Access ============
arrayAccess
    : expression '[' expression ']'
    ;

// ============ Comments ============
comment
    : SINGLE_LINE_COMMENT
    | MULTI_LINE_COMMENT
    ;

// ============ Identifiers ============
identifier
    : IDENTIFIER
    ;

// ============ Lexer Rules ============

// Keywords
SERVER: 'server';
NETWORK: 'network';
DATABASE: 'database';
NOSQL_DB: 'nosql_db';
SECURITY_GROUP: 'security_group';
LOAD_BALANCER: 'load_balancer';
CACHE: 'cache';
CONTAINER: 'container';
FUNCTION: 'function';
SUBNET: 'subnet';
MODULE: 'module';
VARIABLE: 'variable';
CONSTANT: 'constant';
ROLE: 'role';
POLICY: 'policy';
IF: 'if';
ELSE: 'else';
FOR: 'in';
USE: 'use';
WITH: 'with';
CONNECT: 'connect';
ATTACH: 'attach';
TO: 'to';
ASSIGN: 'assign';
USER: 'user';
GROUP: 'group';
PARAM: 'param';
RETURN: 'return';
TRUE: 'true';
FALSE: 'false';
NULL: 'null';
AND: 'and';
OR: 'or';
NOT: 'not';

// Attribute names
TYPE: 'type';
DEFAULT: 'default';
DESCRIPTION: 'description';
PERMISSIONS: 'permissions';
RESOURCES: 'resources';
CONDITIONS: 'conditions';
TARGET: 'target';
RULES: 'rules';
METRICS: 'metrics';
ALARMS: 'alarms';
SCHEDULE: 'schedule';
RETENTION_DAYS: 'retention_days';
BACKUP_RETENTION: 'backup_retention';
SCALE_UP_COOLDOWN: 'scale_up_cooldown';
SCALE_DOWN_COOLDOWN: 'scale_down_cooldown';
LOG_GROUPS: 'log_groups';
LOG_STREAMS: 'log_streams';
MIN_INSTANCES: 'min_instances';
MAX_INSTANCES: 'max_instances';
DESIRED_CAPACITY: 'desired_capacity';

// Resource types
CPU: 'cpu';
MEMORY: 'memory';
OS: 'os';
ENGINE: 'engine';
VERSION: 'version';
STORAGE: 'storage';
INSTANCE_CLASS: 'instance_class';
CIDR_BLOCK: 'cidr_block';
ENABLE_DNS_HOSTNAMES: 'enable_dns_hostnames';
ENABLE_DNS_SUPPORT: 'enable_dns_support';
AVAILABILITY_ZONE: 'availability_zone';
PUBLIC: 'public';
MAP_PUBLIC_IP_ON_LAUNCH: 'map_public_ip_on_launch';
INGRESS: 'ingress';
EGRESS: 'egress';
FROM_PORT: 'from_port';
TO_PORT: 'to_port';
PROTOCOL: 'protocol';
SECURITY_GROUPS: 'security_groups';
CIDR_BLOCKS: 'cidr_blocks';
VPC: 'vpc';
SUBNET_GROUP: 'subnet_group';
VPC_SECURITY_GROUP_IDS: 'vpc_security_group_ids';
NODE_TYPE: 'node_type';
NUM_CACHE_NODES: 'num_cache_nodes';
PORT: 'port';
SUBNET_GROUP_NAME: 'subnet_group_name';
AUTOMATIC_FAILOVER: 'automatic_failover';
MULTI_AZ_ENABLED: 'multi_az_enabled';
READ_REPLICA_COUNT: 'read_replica_count';
MULTI_AZ: 'multi_az';
BACKUP_WINDOW: 'backup_window';
MAINTENANCE_WINDOW: 'maintenance_window';
STORAGE_TYPE: 'storage_type';
STORAGE_ENCRYPTED: 'storage_encrypted';
PARAMETERS: 'parameters';
TAGS: 'tags';
ENABLED: 'enabled';
MONITORING: 'monitoring';
ALGORITHM: 'algorithm';
TARGET_SERVERS: 'target_servers';
LISTENERS: 'listeners';
CERTIFICATE_ARN: 'certificate_arn';
DEFAULT_ACTION: 'default_action';
HEALTH_CHECK: 'health_check';
PATH: 'path';
INTERVAL: 'interval';
TIMEOUT: 'timeout';
HEALTHY_THRESHOLD: 'healthy_threshold';
UNHEALTHY_THRESHOLD: 'unhealthy_threshold';
METRIC: 'metric';
THRESHOLD: 'threshold';
COMPARISON: 'comparison';
STATISTIC: 'statistic';
PERIOD: 'period';
EVALUATION_PERIODS: 'evaluation_periods';
ADJUSTMENT_TYPE: 'adjustment_type';
SCALING_ADJUSTMENT: 'scaling_adjustment';
COLD_STORAGE_AFTER_DAYS: 'cold_storage_after_days';
DELETE_AFTER_DAYS: 'delete_after_days';
LIFECYCLE: 'lifecycle';
TRANSITION_TO_IA: 'transition_to_ia';
TRANSITION_TO_GLACIER: 'transition_to_glacier';
TRANSITION_TO_DEEP_ARCHIVE: 'transition_to_deep_archive';
NAME: 'name';
FILTER_PATTERN: 'filter_pattern';
SOURCE_IP: 'aws:SourceIp';
SOFTWARE: 'software';
ALARM_ACTIONS: 'alarm_actions';
TRANSITION: 'transition';

// Literals
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
INTEGER: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;
STRING: '"' ( ~["\\] | '\\' . )* '"';
SIZE: [0-9]+ ('KB' | 'MB' | 'GB' | 'TB');

// Operators
PLUS: '+';
MINUS: '-';
MULTIPLY: '*';
DIVIDE: '/';
MODULO: '%';
POWER: '**';
EQUALS: '==';
NOT_EQUALS: '!=';
LESS_THAN: '<';
LESS_THAN_OR_EQUAL: '<=';
GREATER_THAN: '>';
GREATER_THAN_OR_EQUAL: '>=';
ASSIGN: '=';
ARROW: '->';
DOT: '.';
COMMA: ',';
SEMICOLON: ';';
COLON: ':';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACKET: '[';
RBRACKET: ']';

// Comments
SINGLE_LINE_COMMENT: '#' ~[\r\n]*;
MULTI_LINE_COMMENT: '/*' .*? '*/';

// Whitespace
WS: [ \t\r\n]+ -> skip;

// ============ Precedence Rules ============

// Expression precedence (highest to lowest):
// 1. Primary expressions (literals, identifiers, function calls, parenthesized expressions)
// 2. Member access and array access
// 3. Unary operators (+, -, not)
// 4. Multiplicative operators (*, /, %)
// 5. Additive operators (+, -)
// 6. Relational operators (<, <=, >, >=)
// 7. Equality operators (==, !=)
// 8. Logical AND (and)
// 9. Logical OR (or)
// 10. Assignment (=)
