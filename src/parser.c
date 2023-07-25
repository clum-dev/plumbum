/**
 * TODO:
 *  -   
 *  -   
 *  -   
*/


#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <ctype.h>

#include "clum-lib/clum-lib.h"
#include "token.h"
#include "parser.h"


void debug_sep() {
    printf("\n");
    line_sep('-', 30);
    printf("\n");
}


//
bool is_disallowed_token(TokenID id) {
    
    // don't allow any (temp) token that will be added in the parsing process
    switch (id) {
        case T_ID:
            return true;
        case T_LINEBREAK:
            return true;
        case T_EOF:
            return true;
        
        case T_STR_LIT:
            return true;
        case T_INT_LIT:
            return true;
        case T_FLOAT_LIT:
            return true;

        default:
            return false;
    }

    return false;
}

//
void add_str_ref(Dict* lookup, TokenSet* tokens, TokenSet* refined, size_t* i) {

    tokset_add_from_id(refined, T_STR_REF_BEGIN, 0, 0);
    // (*i)++;
    // (*i)++;
    (*i) += 2;
    while (tokens->toks[*i]->id != T_RBRACE) {
        if (tokens->toks[(*i)+1]->id != T_EOF) {
            if (tokens->toks[(*i)]->id != T_SPACE) {
                tokset_add(refined, tok_clone(tokens->toks[*i]));
            }
        } else {
            error_msg(E_ERROR, 0, "expected closing brace", false);
            break;
        }
        (*i)++;
    }
    (*i)++;

    tokset_add_from_id(refined, T_STR_REF_END, 0, 0);
}

//
void add_str_lit(TokenSet* refined, String* buff) {
    
    String* temp = str_init("");
    for (size_t i = 0; i < buff->len; i++) {
        // Add escape chars
        if (buff->text[i] == '\\') {
            if (i + 1 < buff->len) {
                switch (buff->text[++i]) {
                    case 'n':
                        str_concat_char(temp, '\n');
                        break;
                    case 't':
                        str_concat_char(temp, '\t');
                        break;
                    case '\\':
                        str_concat_char(temp, '\\');
                        break;
                    case '"':
                        str_concat_char(temp, '"');
                        break;
                    
                    default:
                        error_msg(E_ERROR, -1, "invalid escape char", false);
                }
            }
        } else {
            str_concat_char(temp, buff->text[i]);
        }
    }

    tokset_add_from_buff(refined, T_STR_LIT, temp, 0, 0);
    str_free(temp);
}

//
void build_string(Dict* lookup, TokenSet* tokens, TokenSet* refined, size_t* i) {

    String* buff = str_init("");
    (*i)++;
    while (tokens->toks[*i]->id != T_QUOTE) {
        if (tokens->toks[(*i)+1]->id != T_EOF) {
            if (tokens->toks[(*i)+1]->id == T_LBRACE) {
                add_str_lit(refined, buff);
                str_clear(buff);
                
                add_str_ref(lookup, tokens, refined, i);

            } else {
                str_concat_str(buff, tokens->toks[(*i)++]->raw);
            }
        } else {
            error_msg(E_ERROR, 0, "expected closing string quote", false);
            break;
        }
    }

    add_str_lit(refined, buff);
    str_free(buff);
}

//
bool is_number(Token* tok) {
    return tok->raw->len > 0 && isdigit(tok->raw->text[0]);
}

//
bool is_valid_int(String* str) {
    size_t count = 0;
    for (size_t i = 0; i < str->len; i++) {
        if (isdigit(str->text[i])) {
            count++;
        }
    }
    return count == str->len;
}

//
void add_num_lit(TokenSet* tokens, TokenSet* refined, size_t* i) {

    size_t isFloat = 0;
    String* result = str_init("");
    while (is_valid_int(tokens->toks[*i]->raw) || tokens->toks[*i]->id == T_DOT) {
        Token* current = tokens->toks[*i];
        Token* next = tokens->toks[(*i)+1];
        
        // Track decimals
        if (current->id == T_DOT) {
            isFloat++;

            // No number after decimal - invalid float
            if (!is_valid_int(next->raw)) {
                isFloat++;
                break;
            }
        }

        str_concat_str(result, tokens->toks[*i]->raw);

        if (!(is_valid_int(next->raw) || next->id == T_DOT)) {
            break;
        }

        (*i)++;
    }

    if (isFloat == 0) {
        tokset_add_from_buff(refined, T_INT_LIT, result, 0, 0);
    } else if (isFloat == 1) {
        tokset_add_from_buff(refined, T_FLOAT_LIT, result, 0, 0);
    } else {
        error_msg(E_ERROR, -1, "invalid number literal", false);
    }

    str_free(result);
}

//
void add_unknown(TokenSet* tokens, TokenSet* refined, size_t* i) {
    // Handle numbers
    if (is_number(tokens->toks[*i])) {
        add_num_lit(tokens, refined, i);
    
    // Otherwise add as identifier
    } else {
        tokset_add_from_buff(refined, T_ID, tokens->toks[*i]->raw, 0, 0);
    }
}

//
void parse_file(File* f, Dict* lookup, TokenSet* tokens) {

    printf("Begin matching\n\n");
    while (file_has_next(f)) {
        String* line = file_next(f);
        String* buff = str_init("");

        for (size_t i = 0; i < line->len; i++) {
            String* c1 = str_slice(line, i, i);
            String* c2 = str_slice(line, i, i+1);

            // debug            
            printf("c1: ");
            str_print(c1, false);
            printf("\tc2: ");
            str_print(c2, false);
            printf("\tbuff: ");
            str_print(buff, false);

            TokenID id = T_LOWER_BOUND;
            if (c2 != NULL && dict_contains(lookup, c2)) {
                id = dict_get(lookup, c2)->data->nodedata.hashnode->data->nodedata.var->data.i;
                i++;    // skip 2nd char of c2
            } else if (c1 != NULL && dict_contains(lookup, c1)) {
                id = dict_get(lookup, c1)->data->nodedata.hashnode->data->nodedata.var->data.i;
            } else if (dict_contains(lookup, buff)) {
                id = dict_get(lookup, buff)->data->nodedata.hashnode->data->nodedata.var->data.i;
                str_clear(buff);
            }
            
            else {
                str_concat_str(buff, c1);
            }


            if (id != T_LOWER_BOUND && !is_disallowed_token(id)) {    
                if (dict_contains(lookup, buff)) {
                    TokenID buffID = dict_get(lookup, buff)->data->nodedata.hashnode->data->nodedata.var->data.i;
                    tokset_add_from_id(tokens, buffID, 0, 0);
                    // debug
                    String* bufftemp = tok_get_id_str(buffID);
                    printf("\tmatch: %s", bufftemp->text);
                    str_free(bufftemp);
                } else {
                    tokset_add_from_buff(tokens, T_UNKNOWN, buff, 0, 0);
                    // debug
                    printf("\tadd buff: `%s`", buff->text);
                }
                str_clear(buff);

                tokset_add_from_id(tokens, id, 0, 0);   // todo line/col stuff
                // debug
                String* temp = tok_get_id_str(id);
                printf("\tmatch: %s", temp->text);
                str_free(temp);
            }

            str_free(c1);
            str_free(c2);

            // debug
            printf("\n");
            line_sep('-', 40);
        }

        if (dict_contains(lookup, buff)) {
            TokenID buffID = dict_get(lookup, buff)->data->nodedata.hashnode->data->nodedata.var->data.i;
            tokset_add_from_id(tokens, buffID, 0, 0);
        } else {
            tokset_add_from_buff(tokens, T_UNKNOWN, buff, 0, 0);
        }

        tokset_add_from_id(tokens, T_LINEBREAK, 0, 0);

        str_free(buff);
    }

    tokset_add_from_id(tokens, T_EOF, 0, 0);
}

//
bool is_top_level(TokenID id) {
    return id == T_FUNC_KW || id == T_STRUCT_KW || id == T_ENUM_KW || id == T_CONST_KW || id == T_USING_KW;
}

//
void track_top_level(ProgData* data, Token* tok) {
    // if (is_top_level(tok->id)) {
    //     data->topLvlCount++;
    // }
    switch (tok->id) {
        case T_FUNC_KW:
            data->counts->funcCount++;
            break;
        case T_STRUCT_KW:
            data->counts->structCount++;
            break;
        case T_ENUM_KW:
            data->counts->enumCount++;
            break;
        case T_CONST_KW:
            data->counts->constCount++;
            break;
        case T_USING_KW:
            data->counts->usingCount++;
            break;
        
        default:
            // nothing
            break;
    }
}

//
TokenSet* refine_tokens(Dict* lookup, TokenSet* tokens, ProgData* data) {

    TokenSet* refined = tokset_init();

    for (size_t i = 0; i < tokens->size; i++) {
        track_top_level(data, tokens->toks[i]);
        
        if (tokens->toks[i]->id == T_HASH) {
            while (tokens->toks[i]->id != T_LINEBREAK) {
                i++;
            }
        }

        if (tokens->toks[i]->id != T_SPACE) {  
            if (tokens->toks[i]->id == T_QUOTE) {
                build_string(lookup, tokens, refined, &i);
            } else if (tokens->toks[i]->id == T_UNKNOWN) {
                add_unknown(tokens, refined, &i);  // TODO
            } else {
                tokset_add(refined, tok_clone(tokens->toks[i]));
            }

        }
    }

    return refined;
}


//
ProgData* progdata_init() {
    ProgData* data = (ProgData*)malloc(sizeof(ProgData));

    data->counts = (TopLvlCounts*)malloc(sizeof(TopLvlCounts));
    data->counts->funcCount = 0;
    data->counts->structCount = 0;
    data->counts->enumCount = 0;
    data->counts->constCount = 0;
    data->counts->usingCount = 0;

    data->lookups = (TopLvlLookups*)malloc(sizeof(TopLvlLookups));
    data->lookups->funcs = NULL;
    data->lookups->structs = NULL;
    data->lookups->enums = NULL;
    data->lookups->consts = NULL;
    data->lookups->usings = NULL;

    return data;
}

//
void progdata_free(ProgData* data) {
    if (data != NULL) {
        if (data->counts != NULL) {
            free(data->counts);
            data->counts = 0;
        }
        if (data->lookups != NULL) {
            dict_free(data->lookups->funcs);
            dict_free(data->lookups->structs);
            dict_free(data->lookups->enums);
            dict_free(data->lookups->consts);
            dict_free(data->lookups->usings);

            free(data->lookups);
            data->lookups = NULL;
        }
    }
    free(data);
    data = NULL;
}

//
void track_ids(TokenSet* refined, ProgData* data) {
    data->lookups->funcs = dict_init(data->counts->funcCount, true);
    data->lookups->structs = dict_init(data->counts->structCount, true);
    data->lookups->enums = dict_init(data->counts->enumCount, true);
    data->lookups->consts = dict_init(data->counts->constCount, true);
    data->lookups->usings = dict_init(data->counts->usingCount, true);
    
    for (size_t i = 0; i < refined->size; i++) {

    }
}



//
int main() {

    // Read file
    File* f = file_read("test.pb");
    // File* f = file_read("test2.pb");

    // // debug
    // printf("Stored file:\n\n");
    // while (file_has_next(f)) {
    //     printf("%s\n", file_next(f)->text);
    // }
    // file_rewind(f);
    // debug_sep();

    // Generate symbol lookup table
    // printf("Generate lookup:\n\n");
    Dict* lookup = token_generate_lookup();
    // debug_sep(); 

    // Set of tokens for the program
    TokenSet* tokens = tokset_init();
    
    // Parse file into tokens
    parse_file(f, lookup, tokens);

    // // debug
    // debug_sep();
    // printf("Matched tokens:\n");
    // tokset_print(tokens, false);
    // printf("\n");
    // tokset_print_ids(tokens, true);
    // debug_sep();

    // Init program data tracker
    ProgData* data = progdata_init();

    // Refine generated tokens
    TokenSet* refined = refine_tokens(lookup, tokens, data);
    printf("Refined tokens:\n\n");
    tokset_print(refined, true);
    printf("\n");
    tokset_print_ids(refined, true);
    debug_sep();
    
    // Track identifiers
    // TODO
    
    // Debug
    printf("Prog data:\n");
    printf("funcs: %ld\n", data->counts->funcCount);
    printf("structs: %ld\n", data->counts->structCount);
    printf("enums: %ld\n", data->counts->enumCount);
    printf("consts: %ld\n", data->counts->constCount);
    printf("usings: %ld\n", data->counts->usingCount);

    track_ids(refined, data);

    // Free memory
    
    
    progdata_free(data);

    tokset_free(refined);
    tokset_free(tokens);
    dict_free(lookup);

    file_free(f);

    return 0;
}