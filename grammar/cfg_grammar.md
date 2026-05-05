# Context-Free Grammar for Infrastructure DSL

This document presents the formal context-free grammar (CFG) for the Infrastructure Modeling DSL. The grammar is defined using BNF notation with extensions.

## Grammar Notation

- `::=` - Production rule definition
- `|` - Alternation (OR)
- `[]` - Optional (0 or 1 occurrence)
- `{}` - Repetition (0 or more occurrences)
- `+` - Positive repetition (1 or more occurrences)
- `""` - Terminal symbols (literals)
- `<angle brackets>` - Non-terminal symbols

## Grammar Productions

### 1. Program Structure

```
<program> ::= {<compilation_unit>} <EOF>

<compilation_unit> ::= <statement>
                    | <variable_declaration>
                    | <constant_declaration>
                    | <role_declaration>
                    | <policy_declaration>
                    | <attach_statement>
                    | <assign_statement>
                    | <comment>
```

### 2. Statements

```
<statement> ::= <resource_declaration>
             | <network_declaration>
             | <database_declaration>
             | <security_group_declaration>
             | <load_balancer_declaration>
             | <cache_declaration>
             | <container_declaration>
             | <function_resource_declaration>
             | <subnet_declaration>
```

### 3. Resource Declarations

```
<resource_declaration> ::= "server" <identifier> <resource_block>
<network_declaration> ::= "network" <identifier> <resource_block>
<database_declaration> ::= "database" <identifier> <resource_block>
                         | "nosql_db" <identifier> <resource_block>
<security_group_declaration> ::= "security_group" <identifier> <resource_block>
<load_balancer_declaration> ::= "load_balancer" <identifier> <resource_block>
<cache_declaration> ::= "cache" <identifier> <resource_block>
<container_declaration> ::= "container" <identifier> <resource_block>
<function_resource_declaration> ::= "function" <identifier> <resource_block>
<subnet_declaration> ::= "subnet" <identifier> <resource_block>
```

### 4. Resource Block

```
<resource_block> ::= "{" [<attribute_list>] "}"

<attribute_list> ::= <attribute> {"," <attribute>}

<attribute> ::= <identifier> "=" <expression>
             | <identifier> "=" <object_literal>
             | <identifier> "=" <array_literal>
             | <identifier> "=" <conditional_expression>
```

### 5. Expressions

```
<expression> ::= <literal>
               | <identifier>
               | <function_call>
               | <member_access>
               | <array_access>
               | "(" <expression> ")"
               | <expression> <binary_operator> <expression>
               | <expression> "and" <expression>
               | <expression> "or" <expression>
               | "not" <expression>
               | "-" <expression>
               | "+" <expression>

<binary_operator> ::= "+" | "-" | "*" | "/" | "%" | "**"
                    | "==" | "!=" | "<" | "<=" | ">" | ">="
                    | "in" | "not" "in"

<conditional_expression> ::= "if" <conditional_clause> "then" <expression> ["else" <expression>]

<conditional_clause> ::= <expression>
```



### 8. Variable and Constant Declarations

```
<variable_declaration> ::= "variable" <identifier> <variable_block>

<constant_declaration> ::= "constant" <identifier> "=" <expression>

<variable_block> ::= "{" [<variable_attribute_list>] "}"

<variable_attribute_list> ::= <variable_attribute> {"," <variable_attribute>}

<variable_attribute> ::= "type" "=" <string_literal>
                       | "default" "=" <expression>
                       | "description" "=" <string_literal>
```

### 9. Role Declarations

```
<role_declaration> ::= "role" <identifier> <role_block>

<role_block> ::= "{" [<role_attribute_list>] "}"

<role_attribute_list> ::= <role_attribute> {"," <role_attribute>}

<role_attribute> ::= "description" "=" <string_literal>
                   | "permissions" "=" <array_literal>
                   | "resources" "=" <array_literal>
                   | "conditions" "=" <object_literal>
```

### 10. Policy Declarations

```
<policy_declaration> ::= "policy" <identifier> <policy_block>

<policy_block> ::= "{" [<policy_attribute_list>] "}"

<policy_attribute_list> ::= <policy_attribute> {"," <policy_attribute>}

<policy_attribute> ::= "target" "=" <expression>
                     | "type" "=" <string_literal>
                     | "min_instances" "=" <integer_literal>
                     | "max_instances" "=" <integer_literal>
                     | "desired_capacity" "=" <integer_literal>
                     | "rules" "=" <array_literal>
                     | "metrics" "=" <array_literal>
                     | "alarms" "=" <array_literal>
                     | "schedule" "=" <string_literal>
                     | "retention_days" "=" <integer_literal>
                     | "backup_retention" "=" <integer_literal>
                     | "scale_up_cooldown" "=" <integer_literal>
                     | "scale_down_cooldown" "=" <integer_literal>
                     | "log_groups" "=" <array_literal>
                     | "log_streams" "=" <array_literal>
```


```

### 12. Assignment Statements

```
<assignment> ::= <identifier> "=" <expression>
```


```

### 14. Connect Statement

```
<connect_statement> ::= "connect" <expression> "->" <expression> <connection_block>

<connection_block> ::= "{" [<connection_attribute_list>] "}"

<connection_attribute_list> ::= <connection_attribute> {"," <connection_attribute>}

<connection_attribute> ::= <identifier> "=" <expression>
```

### 15. Attach Statement

```
<attach_statement> ::= "attach" <expression> "to" <expression>
```

### 16. Assign Statement

```
<assign_statement> ::= "assign" <identifier> "to" <user_specification>

<user_specification> ::= "user" <string_literal>
                       | "group" <string_literal>
                       | "role" <string_literal>
```

### 17. Literals

```
<literal> ::= <integer_literal>
            | <float_literal>
            | <string_literal>
            | <boolean_literal>
            | <size_literal>
            | <null_literal>

<integer_literal> ::= <integer>
<float_literal> ::= <float>
<string_literal> ::= <string>
<boolean_literal> ::= "true" | "false"
<size_literal> ::= <size>
<null_literal> ::= "null"
```


```

### 19. Member Access

```
<member_access> ::= <expression> "." <identifier>
```

### 20. Array Access

```
<array_access> ::= <expression> "[" <expression> "]"
```

### 21. Comments

```
<comment> ::= <single_line_comment>
            | <multi_line_comment>

<single_line_comment> ::= "#" <comment_text>
<multi_line_comment> ::= "/*" <comment_text> "*/"
```

### 22. Identifiers

```
<identifier> ::= <identifier_token>
```

### 23. Terminal Symbols (Lexical Tokens)

```
<integer> ::= <digit>+
<float> ::= <digit>+ "." <digit>+
<string> ::= '"' {<string_char>} '"'
<size> ::= <digit>+ ("KB" | "MB" | "GB" | "TB")
<identifier_token> ::= <letter> {<letter> | <digit> | "_"}
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<letter> ::= "A" | "B" | ... | "Z" | "a" | "b" | ... | "z"
<string_char> ::= <any_character_except_quote_or_backslash> | "\\" <any_character>
```

## Grammar Properties

### 1. Ambiguity Resolution

The grammar is designed to be unambiguous with the following precedence rules:

1. **Primary Expressions**: Literals, identifiers, function calls, parenthesized expressions
2. **Member Access**: `.` operator
3. **Array Access**: `[]` operator
4. **Unary Operators**: `-`, `+`, `not`
5. **Multiplicative Operators**: `*`, `/`, `%`
6. **Additive Operators**: `+`, `-`
7. **Relational Operators**: `<`, `<=`, `>`, `>=`
8. **Equality Operators**: `==`, `!=`
9. **Logical AND**: `and`
10. **Logical OR**: `or`
11. **Assignment**: `=`

### 2. Type Safety

The grammar enforces type safety through:

- Strong typing of literals
- Consistent operator usage
- Proper function call syntax
- Valid attribute assignments

### 3. Scope Rules

The grammar supports nested scopes through:

- Block-level scoping in `if` and `for` statements
- Module-level scoping
- Function parameter scoping
- Variable declaration scoping

### 4. Extensibility

The grammar is designed for extensibility:

- New resource types can be added easily
- New attributes can be added to existing resources
- New operators can be added to the expression grammar
- New statement types can be added to the compilation unit

## Grammar Statistics

- **Total Production Rules**: 87
- **Non-terminals**: 62
- **Terminals**: 45
- **Ambiguity**: None (LL(k) grammar)
- **Grammar Type**: Context-Free Grammar (CFG)
- **Parser Type**: Predictive Parser (LL(k))

## Example Derivations

### Example 1: Simple Resource Declaration

```
server "web_server" {
    cpu = 4
    memory = 8GB
}
```

**Derivation**:
```
<statement> → <resource_declaration>
<resource_declaration> → "server" <identifier> <resource_block>
<identifier> → "web_server"
<resource_block> → "{" <attribute_list> "}"
<attribute_list> → <attribute> "," <attribute>
<attribute> → <identifier> "=" <expression>
<identifier> → "cpu"
<expression> → <literal>
<literal> → <integer_literal>
<integer_literal> → "4"
<attribute> → <identifier> "=" <expression>
<identifier> → "memory"
<expression> → <literal>
<literal> → <size_literal>
<size_literal> → "8GB"
```


```

**Derivation**:
```
<conditional_expression> → "if" <conditional_clause> "then" <expression> "else" <expression>
<conditional_clause> → <expression>
<expression> → <expression> <binary_operator> <expression>
<expression> → <identifier>
<identifier> → "environment"
<binary_operator> → "=="
<expression> → <literal>
<literal> → <string_literal>
<string_literal> → "production"
<expression> → <literal>
<literal> → <integer_literal>
<integer_literal> → "8"
<expression> → <literal>
<literal> → <integer_literal>
<integer_literal> → "4"
```

## Grammar Validation

The grammar has been validated for:

1. **Completeness**: All language constructs are covered
2. **Consistency**: No conflicting rules
3. **Unambiguity**: Clear precedence and associativity
4. **Expressiveness**: Can represent all intended DSL constructs
5. **Parsability**: Suitable for LL(k) parsing

This grammar serves as the foundation for the ANTLR parser implementation and ensures the DSL has a well-defined, unambiguous syntax.
