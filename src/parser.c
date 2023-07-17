#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "clum-lib/clum-lib.h"
#include "token.h"
#include "parser.h"


void debug_sep() {
    printf("\n");
    line_sep('-', 30);
    printf("\n");
}


//
ProgData* progdata_init() {
    ProgData* data = (ProgData*)malloc(sizeof(ProgData));
    data->funcCount = 0;
    data->structCount = 0;
    data->enumCount = 0;
    data->constCount = 0;
    data->usingCount = 0;

    data->funcDecls = NULL;
    data->structDecls = NULL;
    data->enumDecls = NULL;
    data->constDecls = NULL;
    data->usingDecls = NULL;

    return data;
}

//
void progdata_free(ProgData* data) {
    if (data != NULL) {
        if (data->funcDecls != NULL) {
            dict_free(data->funcDecls);
            data->funcDecls = NULL;
            data->funcCount = 0;
        }
        if (data->structDecls != NULL) {
            dict_free(data->structDecls);
            data->structDecls = NULL;
            data->structCount = 0;
        }
        if (data->enumDecls != NULL) {
            dict_free(data->enumDecls);
            data->enumDecls = NULL;
            data->enumDecls = 0;
        }
        if (data->constDecls != NULL) {
            dict_free(data->constDecls);
            data->constDecls = NULL;
            data->constCount = 0;
        }
        if (data->usingDecls != NULL) {
            dict_free(data->usingDecls);
            data->usingDecls = NULL;
            data->constCount = 0;
        }

        free(data);
        data = NULL;
    }

}

//
void progdata_print(ProgData* data) {
    printf("Prog data:\n");
    
    printf("Func count: %ld\n", data->funcCount);
    if (data->funcDecls != NULL) {
        dict_print(data->funcDecls, false);
        printf("\n");
    }

    printf("Struct count: %ld\n", data->structCount);
    if (data->structDecls != NULL) {
        dict_print(data->structDecls, false);
    }
    
    printf("Enum count: %ld\n", data->enumCount);
    if (data->enumDecls != NULL) {
        dict_print(data->enumDecls, false);
    }

    printf("Const count: %ld\n", data->constCount);
    if (data->constDecls != NULL) {
        dict_print(data->constDecls, false);
    }

    printf("Using count: %ld\n", data->usingCount);
    if (data->usingDecls != NULL) {
        dict_print(data->usingDecls, false);
    }
    
}

//
void progdata_init_name_lookups(ProgData* data) {
    if (data->funcCount > 0) {
        data->funcDecls = dict_init(data->funcCount, true);
    }
    if (data->structCount > 0) {
        data->structDecls = dict_init(data->structCount, true);
    }
    if (data->enumCount > 0) {
        data->enumDecls = dict_init(data->enumCount, true);
    }
    if (data->constCount > 0) {
        data->constDecls = dict_init(data->constCount, true);
    }
    if (data->usingCount > 0) {
        data->usingDecls = dict_init(data->usingCount, true);
    }
}

//
void progdata_track_top_level(TokenSet* tokens, ProgData* progData, TokenID id, size_t index) {
    
    switch (id) {
        case T_FUNC_KW:
            progData->funcCount++;
            break;
        case T_STRUCT_KW:
            progData->structCount++;
            break;
        case T_ENUM_KW:
            progData->enumCount++;
            break;
        case T_CONST_KW:
            progData->constCount++;
            break;
        case T_USING_KW:
            progData->usingCount++;
            break;
        default:
            // do nothing
            break;
    }
}

//
void progdata_add_entries(TokenSet* refined, ProgData* progData) {
    
    for (size_t i = 0; i < refined->size; i++) {
        // Track program data
        progdata_track_top_level(refined, progData, refined->toks[i]->id, i);
    }
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
TokenID match_token(Dict* lookup, TokenSet* tokens, String* single_c, String* double_c, String* buff, size_t line, size_t* col) {

    TokenID id = T_LOWER_BOUND;

    // Attempt to match the different inputs

    if (double_c != NULL && dict_contains(lookup, double_c)) {
        id = dict_get(lookup, double_c)->data->nodedata.hashnode->data->nodedata.var->data.i;
        *col += 1;
        // printf("match double: %s\t", double_c->text);

    } else if (dict_contains(lookup, single_c)) {
        id = dict_get(lookup, single_c)->data->nodedata.hashnode->data->nodedata.var->data.i;
        // printf("match single: %s\t", single_c->text);
        
    } else if (dict_contains(lookup, buff)) {
        id = dict_get(lookup, buff)->data->nodedata.hashnode->data->nodedata.var->data.i;
        str_clear(buff);
        // printf("match buff: %s\t", buff->text);

    // Otherwise, append the current char to the buffer and continue
    } else {
        str_concat_str(buff, single_c);
        // printf("match undefined\t");
    }

    if (id != T_LOWER_BOUND && !is_disallowed_token(id)) {
        // Check buff for known token
        if (dict_contains(lookup, buff)) {
            size_t idTemp = dict_get(lookup, buff)->data->nodedata.hashnode->data->nodedata.var->data.i;
            tokset_add_from_id(tokens, idTemp, line, *col);
        } else {
            tokset_add_from_buff(tokens, T_UNKNOWN, buff, line, *col);
        }

        str_clear(buff);
        tokset_add_from_id(tokens, id, line, *col);
    }
    
    return id;
}

//
bool skip_all_spaces(TokenSet* tokens, size_t* i) {
    if (tokens->toks[*i]->id != T_LINEBREAK && all_spaces(tokens->toks[*i]->raw->text)) {
        (*i)++;
        return true;
    }
    return false;
}

//
bool skip_comment(TokenSet* tokens, size_t* i) {
    if (tokens->toks[*i]->id == T_HASH) {
        while (tokens->toks[*i]->id != T_LINEBREAK) {
            (*i)++;
        }
        (*i)++;
        return true;
    }
    return false;
}

//
void trim_tok_spaces(Token* tok) {
    String* space = str_init(" ");
    str_reap(tok->raw, space);
    str_free(space);
}

//
void resolve_unknown(TokenSet* tokens, size_t* i, TokenSet* refined) {
    if (tokens->toks[*i]->id != T_UNKNOWN) {
        return;
    } else {
        // Trim spaces
        trim_tok_spaces(tokens->toks[*i]);
    }
}

//
void build_string(TokenSet* tokens, size_t* i, TokenSet* refined) {
        
    // Find quote string
    if (tokens->toks[*i]->id != T_QUOTE) {
        return;

    } else {
                
        (*i)++;
        String* buff = str_init("");
        size_t startLine = tokens->toks[*i]->line;
        size_t startCol = tokens->toks[*i]->col;

        error_msg(E_DEBUG, -1, "Building string lit: start", false);
        tokset_add_from_id(refined, T_STR_LIT_BEGIN, startLine, startCol);

        do {
            printf("token: %s (%s)\n", tokens->toks[*i]->idStr->text, tokens->toks[*i]->raw->text);
            
            if (tokens->toks[*i]->id == T_EOF) {
                error_msg(E_ERROR, -1, "string: expected closing quote", false);
                str_free(buff);
                return;
            }

            // String reference found -> don't add braces
            if (tokens->toks[*i]->id == T_LBRACE) {

                // Add start of string before reference to refined
                if (buff->len > 0) {
                    printf("adding to refined: `%s`\n", buff->text);
                    tokset_add_from_buff(refined, T_STR_LIT, buff, startLine, startCol);
                    str_clear(buff);
                }

                error_msg(E_DEBUG, -1, "Building string ref: start", false);
                tokset_add_from_id(refined, T_STR_REF_BEGIN, startLine, startCol);
                
                // Add everything in the reference (handle later)
                (*i)++;
                do {
                    if (tokens->toks[*i]->id == T_EOF) {
                        error_msg(E_ERROR, -1, "string ref: expected closing brace", false);
                        str_free(buff);
                        return;
                    }
                    printf("adding to refined: `%s`\n", tokens->toks[*i]->raw->text);
                    tokset_add(refined, tok_clone(tokens->toks[*i]));
                    (*i)++;
                } while (tokens->toks[*i]->id != T_RBRACE);
                (*i)++;

                // Reset token position
                startLine = tokens->toks[*i]->line;
                startCol = tokens->toks[*i]->col;

                error_msg(E_DEBUG, -1, "Building string ref: DONE", false);
                tokset_add_from_id(refined, T_STR_REF_END, startLine, startCol);
            }

            // Concat everything (including spaces) -> don't trim
            str_concat_str(buff, tokens->toks[*i]->raw);
            
            // Iterate through string
            (*i)++;
        } while (tokens->toks[*i]->id != T_QUOTE);
        (*i)++;

        // Add combined buffer as token
        printf("adding to refined: `%s`\n", buff->text);
        tokset_add_from_buff(refined, T_STR_LIT, buff, startLine, startCol);
        
        (*i)++;
        str_free(buff);

        error_msg(E_DEBUG, -1, "Building string lit: DONE", false);
        tokset_add_from_id(refined, T_STR_LIT_END, startLine, startCol);
    }
}

//
void add_str_lit(TokenSet* tokset, String* str, size_t startLine, size_t startCol) {
    Token* temp = tok_init(T_STR_LIT, startLine, startCol);
    str_concat_str(temp->raw, str);
    str_concat_char(temp->raw, '`');
    tokset_add(tokset, temp);
}

//
TokenSet* refine_tokens(Dict* lookup, TokenSet* tokens, ProgData* progData) {

    TokenSet* refined = tokset_init();
    for (size_t i = 0; i < tokens->size; i++) {

        // Skip comments
        skip_comment(tokens, &i);

        // Build string if found
        if (tokens->toks[i]->id == T_QUOTE) {
            
            // error_msg(E_DEBUG, -1, "Start string build", false);
                    
            size_t startLine = tokens->toks[i]->line;
            size_t startCol = tokens->toks[i]->col;
            
            String* strlit_raw = str_init("");
            i++;    // Skip opening quote

            do {
                if (tokens->toks[i]->id == T_EOF) {
                    error_msg(E_ERROR, -1, "string: expected closing quote", false);
                    str_free(strlit_raw);
                    return refined;
                }

                //  Build string reference if found
                if (tokens->toks[i]->id == T_LBRACE) {
                    
                    // error_msg(E_DEBUG, -1, "Start string ref build", false);
                    
                    // Add string lit token before ref
                    add_str_lit(refined, strlit_raw, startLine, startCol);
                    str_clear(strlit_raw);  // Clear for str lit after ref
                    
                    tokset_add_from_id(refined, T_STR_REF_BEGIN, tokens->toks[i]->line, tokens->toks[i]->col);
                    i++;    // Skip opening brace

                    do {
                        if (tokens->toks[i]->id == T_EOF) {
                            error_msg(E_ERROR, -1, "string ref: expected closing brace", false);
                            str_free(strlit_raw);
                            return refined;
                        }
                        
                        if (tokens->toks[i]->id == T_UNKNOWN) {
                            Token* temp = tok_init(T_ID, tokens->toks[i]->line, tokens->toks[i]->col);
                            str_concat_str(temp->raw, tokens->toks[i]->raw);
                            tokset_add(refined, temp);
                        } else {
                            tokset_add(refined, tok_clone(tokens->toks[i]));
                        }
                        
                        i++;    // Iterate through string lit
                    } while (tokens->toks[i]->id != T_RBRACE);

                    tokset_add_from_id(refined, T_STR_REF_END, tokens->toks[i]->line, tokens->toks[i]->col);
                    i++;    // Skip closing brace

                    // error_msg(E_DEBUG, -1, "End string ref build", false);

                    continue;
                }

                str_concat_str(strlit_raw, tokens->toks[i]->raw);
                i++;    // Iterate through string

            } while (tokens->toks[i]->id != T_QUOTE);
            // i++;    // Skip closing quote

            add_str_lit(refined, strlit_raw, startLine, startCol);
            str_free(strlit_raw);

            // error_msg(E_DEBUG, -1, "End string build", false);

        // Don't add spaces        
        } else if (tokens->toks[i]->id != T_SPACE) {
            
            // If unknown, treat as ID
            if (tokens->toks[i]->id == T_UNKNOWN) {
                Token* temp = tok_init(T_ID, tokens->toks[i]->line, tokens->toks[i]->col);
                str_concat_str(temp->raw, tokens->toks[i]->raw);
                tokset_add(refined, temp);

            // Otherwise, add normally
            } else {
                tokset_add(refined, tok_clone(tokens->toks[i]));
            }
        }
    }

    return refined;
}


//
int main() {

    // Read file
    File* f = file_read("test.pb");

    // debug
    printf("Stored file:\n\n");
    while (file_has_next(f)) {
        printf("%s\n", file_next(f)->text);
    }
    file_rewind(f);
    debug_sep();

    // Generate symbol lookup table
    printf("Generate lookup:\n\n");
    Dict* lookup = token_generate_lookup();
    debug_sep();

    // // debug - check all tokens are set in dictionary
    // for (size_t i = T_LOWER_BOUND + 1; i < T_UPPER_BOUND; i++) {
    //     if (i == T_UNKNOWN) {
    //         continue;
    //     }

    //     String* tempKey = tok_get_raw_str(i);
    //     String* tempName = tok_get_id_str(i);
    //     printf("[%s]\tcontains %s\t", tempName->text, tempKey->text);
    //     if (dict_contains(lookup, tempKey)) {
    //         printf("TRUE");
    //     } else {
    //         printf("FALSE");
    //     }
    //     printf("\n");
    //     str_free(tempName);
    //     str_free(tempKey);
    // }


    // // debug
    // debug_sep();
    // printf("Lookup dictionary:\n");
    // dict_print(lookup, false);
    // debug_sep();
    

    // Program data
    ProgData* progData = progdata_init();

    // Set of tokens for the program
    TokenSet* tokens = tokset_init();
    
    // Iterate through file lines
    printf("Begin matching:\n\n");
    while (file_has_next(f)) {

        String* line = file_next(f);
        String* buff = str_init("");

        // Iterate through line
        for (size_t i = 0; i < line->len; i++) {
            
            char c = line->text[i];
            char c2 = '\0';
            if (i + 1 < line->len) {
                c2 = line->text[i + 1];
            }
            
            // Next char
            String* single_c = str_init("");
            str_concat_char(single_c, c);
            
            // Next 2 chars
            String* double_c = NULL;
            if (c2 != '\0') {
                double_c = str_init(single_c->text);
                str_concat_char(double_c, c2);
            }           

            // debug
            printf("buff: `%s`\t", buff->text);
            printf("single: `%s`\t", single_c->text);
            if (double_c != NULL) {
                printf("double: `%s`\t", double_c->text);
            } else {
                printf("double: `NULL`\t");
            }


            // Match token
            TokenID id = match_token(lookup, tokens, single_c, double_c, buff, f->currentLine, &i);
            
            // debug
            String* temp = tok_get_id_str(id);
            if (!str_equals_text(temp, "T_UNDEFINED", true)) {
                printf("\t (%s)", temp->text);
            }
            printf("\n");
            str_free(temp);


            str_free(single_c);
            str_free(double_c);

        }

        // Reached end, add what's left
        if (dict_contains(lookup, buff)) {
            size_t idTemp = dict_get(lookup, buff)->data->nodedata.hashnode->data->nodedata.var->data.i;
            tokset_add_from_id(tokens, idTemp, f->currentLine, line->len);
        } else {
            tokset_add_from_buff(tokens, T_UNKNOWN, buff, f->currentLine, line->len);
        }

        // Add newline token at end of each line
        tokset_add_from_id(tokens, T_LINEBREAK, f->currentLine, line->len);

        str_free(buff);
    }


    // Append eof to tokset
    tokset_add_from_id(tokens, T_EOF, f->lines->size, 0);


    // debug
    debug_sep();
    printf("Matched tokens:\n");
    tokset_print(tokens, false);
    printf("\n");
    tokset_print_ids(tokens);
    debug_sep();


    // Refine generated tokens
    TokenSet* refined = refine_tokens(lookup, tokens, progData);
    printf("Refined tokens:\n");
    tokset_print(refined, true);
    printf("\n");
    tokset_print_ids(refined);
    debug_sep();

    // Update program data with top level names
    progdata_init_name_lookups(progData);
    progdata_add_entries(refined, progData);

    // debug
    progdata_print(progData);
    debug_sep();

    tokset_free(refined);
    tokset_free(tokens);
    dict_free(lookup);
    progdata_free(progData);

    file_free(f);

    return 0;
}