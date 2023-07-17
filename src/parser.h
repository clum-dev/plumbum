#ifndef __PARSER_H__
#define __PARSER_H__

#include "clum-lib/clum-lib.h"

typedef struct ProgData {

    // Track top level declarations
    size_t funcCount;
    size_t structCount;
    size_t enumCount;
    size_t constCount;
    size_t usingCount;

    Dict* funcDecls;
    Dict* structDecls;
    Dict* enumDecls;
    Dict* constDecls;
    Dict* usingDecls;



} ProgData;




#endif