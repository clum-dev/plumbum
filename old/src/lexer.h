#ifndef __LEXER_H__
#define __LEXER_H__

#include "clum-lib/clum-lib.h"

typedef struct TopLvlCounts {
    size_t funcCount;
    size_t structCount;
    size_t enumCount;
    size_t constCount;
    size_t usingCount;
} TopLvlCounts;

typedef struct TopLvlLookups {
    Dict* funcs;
    Dict* structs;
    Dict* enums;
    Dict* consts;
    Dict* usings;
} TopLvlLookups;


typedef struct ProgData {

    TopLvlCounts* counts;
    TopLvlLookups* lookups;

} ProgData;



#endif