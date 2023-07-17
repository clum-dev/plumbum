#include <stdio.h>
#include <stdlib.h>

#include "token.h"

//
String* tok_get_id_str(TokenID id) {
    switch (id) {
        // PARSING SYMBOLS
        case T_UNKNOWN:
            return str_init("T_UNKNOWN");
        case T_ID:
            return str_init("T_ID");
        case T_SPACE:
            return str_init("T_SPACE");
        case T_LINEBREAK:
            return str_init("T_LINEBREAK");
        case T_EOF:
            return str_init("T_EOF");

        case T_STR_LIT_BEGIN:
            return str_init("T_STR_LIT_BEGIN");
        case T_STR_LIT_END:
            return str_init("T_STR_LIT_END");
        case T_STR_REF_BEGIN:
            return str_init("T_STR_REF_BEGIN");
        case T_STR_REF_END:
            return str_init("T_STR_REF_END");

        case T_STR_LIT:
            return str_init("T_STR_LIT");
        case T_INT_LIT:
            return str_init("T_INT_LIT");
        case T_FLOAT_LIT:
            return str_init("T_FLOAT_LIT");
        case T_TRUE:
            return str_init("T_TRUE");
        case T_FALSE:
            return str_init("T_FALSE");

        // TOP LEVEL KEYWORDS
        case T_FUNC_KW:
            return str_init("T_FUNC_KW");
        case T_STRUCT_KW:
            return str_init("T_STRUCT_KW");
        case T_ENUM_KW:
            return str_init("T_ENUM_KW");
        case T_CONST_KW:
            return str_init("T_CONST_KW");
        case T_USING_KW:
            return str_init("T_USING_KW");

        // CONTROL FLOW
        case T_IF:
            return str_init("T_IF");
        case T_ELSE:
            return str_init("T_ELSE");
        case T_FOR:
            return str_init("T_FOR");
        case T_WHILE:
            return str_init("T_WHILE");
        case T_BREAK:
            return str_init("T_BREAK");
        case T_CONTINUE:
            return str_init("T_CONTINUE");
        case T_RETURN:
            return str_init("T_RETURN");

        // MISC SYMBOLS
        case T_HASH:
            return str_init("T_HASH");
        case T_QUOTE:
            return str_init("T_QUOTE");
        case T_COLON:
            return str_init("T_COLON");
        case T_COLON2:
            return str_init("T_COLON2");
        case T_SEMICOLON:
            return str_init("T_SEMICOLON");
        case T_COMMA:
            return str_init("T_COMMA");
        case T_DOLLAR:
            return str_init("T_DOLLAR");
        case T_AMPERSAND:
            return str_init("T_AMPERSAND");
        case T_AT:
            return str_init("T_AT");
        case T_QUESTION:
            return str_init("T_QUESTION");
        case T_UNDERSCORE:
            return str_init("T_UNDERSCORE");
        case T_DOT:
            return str_init("T_DOT");
        case T_DOT2:
            return str_init("T_DOT2");
        case T_RARROW:
            return str_init("T_RARROW");
        case T_BACKSLASH:
            return str_init("T_BACKSLASH");
                
        // BRACKETS
        case T_LPAREN:
            return str_init("T_LPAREN");
        case T_RPAREN:
            return str_init("T_RPAREN");
        case T_LBRACK:
            return str_init("T_LBRACK");
        case T_RBRACK:
            return str_init("T_RBRACK");
        case T_LBRACE:
            return str_init("T_LBRACE");
        case T_RBRACE:
            return str_init("T_RBRACE");
        case T_LANGLE:
            return str_init("T_LANGLE");
        case T_RANGLE:
            return str_init("T_RANGLE");
        
        // MATH OPS
        case T_PLUS:
            return str_init("T_PLUS");
        case T_MINUS:
            return str_init("T_MINUS");
        case T_ASTERISK:
            return str_init("T_ASTERISK");
        case T_SLASH:
            return str_init("T_SLASH");

        case T_PERCENT:
            return str_init("T_PERCENT");
        case T_ASTERISK2:
            return str_init("T_ASTERISK2");
        case T_PLUS2:
            return str_init("T_PLUS2");
        case T_MINUS2:
            return str_init("T_MINUS2");
        
        // COMPARATORS
        case T_EQUAL2:
            return str_init("T_EQUAL2");
        case T_BANGEQUAL:
            return str_init("T_BANGEQUAL");
        case T_RARROWEQUAL:
            return str_init("T_RARROWEQUAL");
        case T_LARROWEQUAL:
            return str_init("T_LARROWEQUAL");

        // PIPES
        case T_PIPE:
            return str_init("T_PIPE");
        case T_PIPEFUNNEL:
            return str_init("T_PIPEFUNNEL");
        case T_PIPEDIST:
            return str_init("T_PIPEDIST");
        case T_PIPEPAIR:
            return str_init("T_PIPEPAIR");
        case T_PIPEMAP:
            return str_init("T_PIPEMAP");
        case T_PIPEFILTER:
            return str_init("T_PIPEFILTER");
        case T_PIPECAST:
            return str_init("T_PIPECAST");
        case T_PIPESUM:
            return str_init("T_PIPESUM");

        // BASIC TYPES
        case T_TYPE_ANY:
            return str_init("T_TYPE_ANY");
        case T_TYPE_INT:
            return str_init("T_TYPE_INT");
        case T_TYPE_FLO:
            return str_init("T_TYPE_FLO");
        case T_TYPE_STR:
            return str_init("T_TYPE_STR");
        case T_TYPE_CHAR:
            return str_init("T_TYPE_CHAR");
        case T_TYPE_BOOL:
            return str_init("T_TYPE_BOOL");
        case T_TYPE_NULL:
            return str_init("T_TYPE_NULL");

        
        default:
            // error_msg(E_ERROR, -1, "Undefined token id", false);
            return str_init("T_UNDEFINED");
    }
}

//
String* tok_get_raw_str(TokenID id) {
    switch (id) {
        case T_UNKNOWN:
            return str_init("[unknown]");
        case T_ID:
            return str_init("ID:");     // TODO: concat actual value
        case T_SPACE:
            return str_init(" ");
        case T_LINEBREAK:
            return str_init("\n");
        case T_EOF:
            return str_init("[EOF]");

        case T_STR_LIT_BEGIN:
            return str_init("[\"");
        case T_STR_LIT_END:
            return str_init("\"]");
        case T_STR_REF_BEGIN:
            return str_init("REF:[\"");
        case T_STR_REF_END:
            return str_init("\"]");

        case T_STR_LIT:
            return str_init("STR:`");
        case T_INT_LIT:
            return str_init("INT:");
        case T_FLOAT_LIT:
            return str_init("FLO:");
        case T_TRUE:
            return str_init("true");
        case T_FALSE:
            return str_init("false");

        // TOP LEVEL KEYWORDS
        case T_FUNC_KW:
            return str_init("func");
        case T_STRUCT_KW:
            return str_init("struct");
        case T_ENUM_KW:
            return str_init("enum");
        case T_CONST_KW:
            return str_init("const");
        case T_USING_KW:
            return str_init("using");

        // CONTROL FLOW
        case T_IF:
            return str_init("if");
        case T_ELSE:
            return str_init("else");
        case T_FOR:
            return str_init("for");
        case T_WHILE:
            return str_init("while");
        case T_BREAK:
            return str_init("break");
        case T_CONTINUE:
            return str_init("continue");
        case T_RETURN:
            return str_init("return");

        // MISC SYMBOLS
        case T_HASH:
            return str_init("#");
        case T_QUOTE:
            return str_init("\"");
        case T_COLON:
            return str_init(":");
        case T_COLON2:
            return str_init("::");
        case T_SEMICOLON:
            return str_init(";");
        case T_COMMA:
            return str_init(",");
        case T_DOLLAR:
            return str_init("$");
        case T_AMPERSAND:
            return str_init("&");
        case T_AT:
            return str_init("@");
        case T_QUESTION:
            return str_init("?");
        case T_UNDERSCORE:
            return str_init("_");
        case T_DOT:
            return str_init(".");
        case T_DOT2:
            return str_init("..");
        case T_RARROW:
            return str_init("->");
        case T_BACKSLASH:
            return str_init("\\");
        
        // BRACKETS
        case T_LPAREN:
            return str_init("(");
        case T_RPAREN:
            return str_init(")");
        case T_LBRACK:
            return str_init("[");
        case T_RBRACK:
            return str_init("]");
        case T_LBRACE:
            return str_init("{");
        case T_RBRACE:
            return str_init("}");
        case T_LANGLE:
            return str_init("<");
        case T_RANGLE:
            return str_init(">");

        // MATH OPS
        case T_PLUS:
            return str_init("+");
        case T_MINUS:
            return str_init("-");
        case T_ASTERISK:
            return str_init("*");
        case T_SLASH:
            return str_init("/");
        
        case T_PERCENT:
            return str_init("%");
        case T_ASTERISK2:
            return str_init("**");
        case T_PLUS2:
            return str_init("++");
        case T_MINUS2:
            return str_init("--");

        // COMPARATORS
        case T_EQUAL2:
            return str_init("==");
        case T_BANGEQUAL:
            return str_init("!=");
        case T_RARROWEQUAL:
            return str_init(">=");
        case T_LARROWEQUAL:
            return str_init("<=");

        // PIPES
        case T_PIPE:
            return str_init("|");
        case T_PIPEFUNNEL:
            return str_init("|>");
        case T_PIPEDIST:
            return str_init("|<");
        case T_PIPEPAIR:
            return str_init("|:");
        case T_PIPEMAP:
            return str_init("|@");
        case T_PIPEFILTER:
            return str_init("|?");
        case T_PIPECAST:
            return str_init("|=");
        case T_PIPESUM:
            return str_init("|+");

        // BASIC TYPES
        case T_TYPE_ANY:
            return str_init("any");
        case T_TYPE_INT:
            return str_init("int");
        case T_TYPE_FLO:
            return str_init("float");
        case T_TYPE_STR:
            return str_init("string");
        case T_TYPE_CHAR:
            return str_init("char");
        case T_TYPE_BOOL:
            return str_init("bool");
        case T_TYPE_NULL:
            return str_init("null");

        
        
        default:
            // error_msg(E_ERROR, -1, (printf("token: %d\n", id), "Undefined token id"), false);
            return str_init("[undefined]");
    }
}


//
Token* tok_init(TokenID id, size_t line, size_t col) {
    Token* tok = (Token*)malloc(sizeof(Token));
    tok->id = id;
    tok->idStr = tok_get_id_str(id);

    tok->raw = tok_get_raw_str(id);
    
    tok->data = NULL;
    tok->next = arr_init(T_INT);    // ids (ints) for next set

    tok->line = line;
    tok->col = col + 1;

    return tok;
}

//
void tok_free(Token* tok) {
    if (tok != NULL) {
        if (tok->idStr != NULL) {
            str_free(tok->idStr);
            tok->idStr = NULL;
        }
        if (tok->raw != NULL) {
            str_free(tok->raw);
            tok->raw = NULL;
        }
        if (tok->next != NULL) {
            arr_free(tok->next);
            tok->next = NULL;
        }

        free(tok);
        tok = NULL;
    }
}

//
Token* tok_clone(Token* tok) {
    Token* out = tok_init(tok->id, tok->line, tok->col);
    return out;    
}

//
TokenSet* tokset_init() {
    TokenSet* tokset = (TokenSet*)malloc(sizeof(TokenSet));
    tokset->toks = NULL;
    tokset->size = 0;
    return tokset;
}

//
void tokset_free(TokenSet* tokset) {
    if (tokset != NULL) {
        for (size_t i = 0; i < tokset->size; i++) {
            tok_free(tokset->toks[i]);
        }
        if (tokset->toks != NULL) {
            free(tokset->toks);
            tokset->toks = NULL;
        }

        free(tokset);
        tokset = NULL;
    }
}

//
void tokset_print(TokenSet* tokset, bool spaceSep) {

    for (size_t i = 0; i < tokset->size; i++) {
        printf("%s", tokset->toks[i]->raw->text);
        if (tokset->toks[i]->id != T_LINEBREAK && spaceSep) {
            printf(" ");
        }
    }

    printf("\n");

}

//
void tokset_print_ids(TokenSet* tokset) {
    for (size_t i = 0; i < tokset->size; i++) {
        printf("%s ", tokset->toks[i]->idStr->text);
        if (tokset->toks[i]->id == T_LINEBREAK) {
            printf("\n");
        }
    }

    printf("\n");

}

//
void tokset_add(TokenSet* tokset, Token* tok) {

    if (tokset->toks == NULL) {
        tokset->toks = (Token**)malloc(sizeof(Token*) * ++tokset->size);
    } else {
        tokset->toks = (Token**)realloc(tokset->toks, sizeof(Token*) * ++tokset->size);
    }

    tokset->toks[tokset->size - 1] = tok;
}

//
void tokset_add_from_id(TokenSet* tokset, TokenID id, size_t line, size_t col) {
    tokset_add(tokset, tok_init(id, line, col));
}

//
void tokset_add_from_buff(TokenSet* tokset, TokenID id, String* buff, size_t line, size_t col) {
    if (buff->len == 0) {
        return;
    }

    // Add unknown token with buffer string
    // Token* temp = tok_init(T_UNKNOWN, line, col);
    
    Token* temp = tok_init(id, line, col);
    str_set(temp->raw, buff->text);
    tokset_add(tokset, temp);
}



//
Dict* token_generate_lookup() {

    Dict* lookup = dict_init(150, true);
    
    for (TokenID t = T_LOWER_BOUND + 1; t < T_UPPER_BOUND; t++) {
        // ID doesn't have a set raw string (could be anything)
        if (t == T_ID) {
            continue;
        }

        // // debug
        // String* msg = str_init("adding token: ");
        // String* idstr = tok_get_id_str(t);
        // str_concat_str(msg, idstr);
        // error_msg(E_DEBUG, t, msg->text, false);
        // str_free(idstr);
        // str_free(msg);

        // Otherwise add entry
        dict_add(lookup, tok_get_raw_str(t), node_init(NODE_VAR, var_from_int((int)t), false));
    }

    return lookup;
}
