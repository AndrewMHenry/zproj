main:
	PUSH	DE
	PUSH	HL
	LD	HL, fontFBF
	CALL	writeSetFont
	CALL	drawClearScreen
	LD	DE, 0
	LD	HL, helloStr
	CALL	writeString
	CALL	screenUpdate
	CALL	keyboardWait
	CALL	drawClearScreen
	CALL	screenUpdate
	POP	HL
	POP	DE
	RET

helloStr:
        .db     "HELLO WORLD!", 0
