#include <stdio.h>
#include <stdlib.h>

#include "token.h"
#include "syntax.h"

//
Token* tok_current(TokenSet* toks, size_t* index) {
    return (*index < toks->size ? toks->toks[*index] : NULL);
}

//
Token* tok_next(TokenSet* toks, size_t* index) {
    return tok_current(toks, ++(*index));
}

//
bool tok_has_next(TokenSet* toks, size_t index) {
    return (tok_next(toks, index) != NULL ? true : false);
}

//
bool match(TokenID match, TokenID* acceptable) {
    return match == acceptable;
}

//
bool match_multi(TokenID match, Arr* acceptable) {
    return (match != NULL && arr_contains(acceptable, tok_get_id_str(match), true) ? true : false);
}



//
bool rule_block(TokenSet* toks, size_t* index) {
    // { PIPES }
    match(tok_current(toks, index), T_LBRACE);
    while (tok_has_next(toks, index)) {
        // if ()
    }

}

//
bool rule_struct(TokenSet* toks, size_t* index) {

}


//
bool rule_top_level(TokenSet* toks, size_t* index) {

    Token* curr = tok_current(toks, index);

    if (curr != NULL && (curr->id == T_FUNC_KW 
            || curr->id == T_STRUCT_KW || curr->id == T_ENUM_KW 
            || curr->id == T_CONST_KW || curr->id == T_USING_KW)) {
        
        TokenID id = curr->id;

        switch (id) {
            case T_FUNC_KW:
                unimp("func kw rule");
                break;
            case T_STRUCT_KW:
                unimp("struct kw rule");
                break;
            case T_ENUM_KW:
                unimp("enum kw rule");
                break;
            case T_CONST_KW:
                unimp("const kw rule");
                break;
            case T_USING_KW:
                unimp("using kw rule");
                break;

            default:
                unimp("error: rule_top_level");
                return false;
        }
    }

    return true;    
}


bool begin_static_check(TokenSet* toks) {

    error_msg(E_INFO, 0, "Begin static checking", false);
    for (size_t index = 0; index < toks->size; index++) {
        rule_top_level(toks, &index);
    }

    error_msg(E_INFO, 0, "End static checking", false);

    return true;    
}
