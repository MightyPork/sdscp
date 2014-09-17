#pragma once
#pragma renderer sds2

// -------------------------- SYSTEM MACROS -----------------------------

// Reference
// - funkce ..... http://wiki.merenienergie.cz/index.php/Sdsc_sysf
// - promenne ... http://wiki.merenienergie.cz/index.php/Sdsc_sysp

#define true 1
#define false 0

// ########## Aliasy systemovych promennych ##########


// uptime (v 10ms)
#define _UPTIME sys[3]

// unix timestamp NTP
#define _TIMESTAMP sys[4]

#define _TIME_DAY sys[5]
#define _TIME_MONTH sys[6]
#define _TIME_YEAR sys[7]
#define _TIME_H sys[8]
#define _TIME_M sys[9]
#define _TIME_S sys[10]

// rychlost, 0..1 krok/ms, 128..max rychlost
#define _SPEED sys[63]

// odpocet sekund, kazkou sekundu se snizi do 0
#define _TIMER sys[64]

#define _OSI7_STATUS sys[65]

#define _HTTP_GET_RESULT sys[75]
#define _HTTP_GET_STATUS _OSI7_STATUS


// === uzivatelske promenne ===
#define _VAR[n] sys[139 + (n)]

// 0..control bez hesla, 1..pozadovat heslo
#define _WEB_ACCESS sys[150]

// 0..ethernet nefunguje, 1..ethernet OK
#define _ETH_WORKS sys[24]


// === trvala pamet ===
#define _FLASH[n] sys[99 + (n)]


// === GPIO D0 port ===

// Hodnoty D0 pinu (8 bitu)
#define _D0  sys[301]

// Smer I/O D0 (1 out, 0 in)
#define _D0_DIR  sys[302]


// === OPTO1 vstup ===

// hodnota 0 = ACTIVE
#define _OPTO[n] sys[150 + (n)]


// === nastaveni PWM ===

// PWM frekvence Hz
#define _PWM_FREQ  sys[191]

// PWM strida (duty factor) - hodnota 0..FREQ
#define _PWM_DUTY  sys[192]


// === cteni 1-WIRE teplomeru ===

// teplota je v C*100
#define _TEMP[n] sys[309 + (n)]
#define _TEMP_STATUS[n] sys[349 + (n)]
#define _TEMP_ROM[n] sys[899 + (n)]


// === vystupy na rele ===
#define _RELAY_ACCESS[n] sys[195 + (n)]
#define _RELAY[n] sys[230 + (n)]
#define _RELAY_NAME[n] sys[265 + (n)]


// === cteni A/D ===

// namerene hodnoty

#define _AD[n] sys[430 + (n)]

// nastaveni na webovem rozhrani
// Pozor! offset je uz odecteny!

#define _AD_OFFSET[n] sys[435 + 4 * (n - 1)]
#define _AD_DIV[n]    sys[436 + 4 * (n - 1)]
#define _AD_NAME[n]   sys[437 + 4 * (n - 1)]
#define _AD_UNIT[n]   sys[438 + 4 * (n - 1)]

// === mereni S0 ===

// tarif
// 0 ... T0 (vysoky),
// 1 ... T1 (nizky)
#define _S0_TARIF  sys[459]

// nastaveni pomeru mericiho transformatoru MTD
#define _S0_MTD[n]  sys[459 + (n)]

// pocitadlo impulzu pro vysoky tarif T0
#define _S0_T0[n]  sys[492 + (n)]

// pocitadlo impulzu pro nizky tarif T1
#define _S0_T1[n]  sys[525 + (n)]

// pocet impulzu na jednotku, napr. 1 kWh (uziv. nastaveni)
#define _S0_UNIT[n]  sys[558 + (n)]

// delka mezery mezi impulzy (ms)
#define _S0_WIDTH[n]  sys[591 + (n)]

// jak dlouho od posledniho impulzu (ms)
#define _S0_WIDTH_ACTUAL[n]  sys[624 + (n)]




// Wait for SYS_TIMER == 0
wait_for_timer()
{
	while(_TIMER != 0);
}

// Wait for http_get()
wait_for_http_get()
{
	echo("Waiting for get.");

	while(_HTTP_GET_STATUS == 0)
		wait(10);
}
