#ifndef __TOKEN_H__
#define __TOKEN_H__

#include "clum-lib/clum-lib.h"

typedef enum TokenID {
    
    T_LOWER_BOUND,  // error

    // PARSING SYMBOLS
    T_UNKNOWN,      // unknown
    T_ID,           // identifier
    T_SPACE,        // ' '
    T_LINEBREAK,    // line break (debug)
    T_EOF,          // end of file (debug)

    T_STR_REF_BEGIN,    // [$
    T_STR_REF_END,      // $]

    T_STR_LIT,      // string literal
    T_INT_LIT,      // int literal
    T_FLOAT_LIT,    // float literal
    T_TRUE,         // true
    T_FALSE,        // false

    // TOP LEVEL KEYWORDS
    T_FUNC_KW,      // func
    T_STRUCT_KW,    // struct
    T_ENUM_KW,      // enum
    T_CONST_KW,     // const
    T_USING_KW,     // using

    // CONTROL FLOW
    T_IF,           // if
    T_ELSE,         // else
    T_FOR,          // for
    T_WHILE,        // while
    T_BREAK,        // break
    T_CONTINUE,     // continue
    T_RETURN,       // return

    // MISC SYMBOLS
    T_HASH,         // #
    T_QUOTE,        // "
    T_COLON,        // :
    T_COLON2,       // ::
    T_SEMICOLON,    // ;
    T_COMMA,        // ,
    T_DOLLAR,       // $
    T_AMPERSAND,    // &
    T_AT,           // @
    T_QUESTION,     // ?
    T_UNDERSCORE,   // _
    T_DOT,          // .
    T_DOT2,         // ..
    T_RARROW,       // ->
    T_BACKSLASH,    /*\*/ 

    // BRACKETS
    T_LPAREN,       // (
    T_RPAREN,       // )
    T_LBRACK,       // [
    T_RBRACK,       // ]
    T_LBRACE,       // {
    T_RBRACE,       // }
    T_LANGLE,       // <
    T_RANGLE,       // >

    // MATH OPS
    T_PLUS,         // +
    T_MINUS,        // -
    T_ASTERISK,     // *
    T_SLASH,        // /
    T_PERCENT,      // %
    T_ASTERISK2,    // **
    T_PLUS2,        // ++
    T_MINUS2,       // --

    // COMPARATORS
    T_EQUAL2,       // ==
    T_BANGEQUAL,    // !=
    T_RARROWEQUAL,  // <=
    T_LARROWEQUAL,  // >=

    // PIPES
    T_PIPE,         // |
    T_PIPEFUNNEL,   // |>
    T_PIPEDIST,     // |<
    T_PIPEPAIR,     // |:
    T_PIPEMAP,      // |@
    T_PIPEFILTER,   // |?
    T_PIPECAST,     // |=
    T_PIPESUM,      // |+

    // BASIC TYPES
    T_TYPE_ANY,     // any
    T_TYPE_INT,     // int
    T_TYPE_FLO,     // flo
    T_TYPE_STR,     // str
    T_TYPE_CHAR,    // char
    T_TYPE_BOOL,    // bool
    T_TYPE_NULL,    // null 
    

    T_UPPER_BOUND,  // error

} TokenID;

//
typedef struct Token {

    TokenID id;
    String* idStr;

    String* raw;

    size_t line;
    size_t col;

    void* data;
    Arr* next;

} Token;

//
typedef struct TokenSet {

    Token** toks;
    size_t size;

} TokenSet;

String* tok_get_id_str(TokenID id);
String* tok_get_raw_str(TokenID id);

Token* tok_init(TokenID id, size_t line, size_t col);
void tok_free(Token* tok);
Token* tok_clone(Token* tok);

TokenSet* tokset_init();
void tokset_print(TokenSet* tokset, bool spaceSep);
void tokset_print_ids(TokenSet* tokset, bool showSpace);
void tokset_free(TokenSet* tokset);
void tokset_add(TokenSet* tokset, Token* tok);
void tokset_add_from_id(TokenSet* tokset, TokenID id, size_t line, size_t col);
// void tokset_add_from_buff(TokenSet* tokset, String* buff, size_t line, size_t col);
void tokset_add_from_buff(TokenSet* tokset, TokenID id, String* buff, size_t line, size_t col);

Dict* token_generate_lookup();

#endif