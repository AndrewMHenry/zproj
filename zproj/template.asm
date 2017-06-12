;;; APP BOILERPLATE

#define APP_NAME "{app_name:8}"
#include "app.asm"


;;; MAIN FILE INCLUSION

#include "{main_file}"


;;; LIBRARY INCLUSIONS

{library_includes}


;;; RESOURCE INCLUSIONS

{resource_includes}


;;; MEMORY EQUATES

{memory_equates}


;;; APPLICATION CODE

appMain:
{init_calls}
        CALL    {entry_point}
{exit_calls}
        RET
