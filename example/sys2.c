#ifndef SYS_C_INCLUDED
#define SYS_C_INCLUDED

// Verze 2, pro SDSCP 1.0+

// -------------------------- SYSTEM MACROS -----------------------------

// Reference
// - funkce ..... http://wiki.merenienergie.cz/index.php/Sdsc_sysf
// - promenne ... http://wiki.merenienergie.cz/index.php/Sdsc_sysp

#define true 1
#define True 1
#define TRUE 1

#define false 0
#define False 0
#define FALSE 0


// ########## Aliasy systemovych promennych ##########



// uptime (v 10ms)
#define SYS_UPTIME sys[3]
#define UPTIME SYS_UPTIME

// unix timestamp NTP
#define SYS_TIMESTAMP sys[4]
#define TIMESTAMP SYS_TIMESTAMP

#define SYS_TIME_DAY sys[5]
#define SYS_TIME_MONTH sys[6]
#define SYS_TIME_YEAR sys[7]
#define SYS_TIME_H sys[8]
#define SYS_TIME_M sys[9]
#define SYS_TIME_S sys[10]

#define TIME_DAY SYS_TIME_DAY
#define TIME_MONTH SYS_TIME_MONTH
#define TIME_YEAR SYS_TIME_YEAR
#define TIME_H SYS_TIME_H
#define TIME_M SYS_TIME_M
#define TIME_S SYS_TIME_S

// rychlost, 0..1 krok/ms, 128..max rychlost
#define SYS_SPEED sys[63]
#define SPEED SYS_SPEED


// odpocet sekund, kazkou sekundu se snizi do 0
#define SYS_TIMER sys[64]
#define TIMER SYS_TIMER

// Wait for SYS_TIMER == 0
wait_for_timer()
{
	while(TIMER != 0);
}


#define SYS_OSI7_STATUS sys[65]
#define OSI7_STATUS sys[65]

#define SMTP_STATUS_OK 256


// Wait for http_get()
wait_for_http_get()
{
	echo("Waiting for get.");

	// do
	while(OSI7_STATUS == 0) {
		wait(10);
	}
}

#define SYS_HTTP_GET_RESULT sys[75]
#define HTTP_GET_RESULT SYS_HTTP_GET_RESULT

#define HTTP_GET_STATUS SYS_OSI7_STATUS

#define HTTP_GET_STATUS_OK 1024 // success

#define HTTP_GET_OK() ((HTTP_GET_STATUS == HTTP_GET_STATUS_OK) && (HTTP_GET_RESULT == 200))


// === uzivatelske promenne ===
#define SYS_VAR[n] sys[139 + (n)]
#define VAR[n] SYS_VAR[n]

// 0..control bez hesla, 1..pozadovat heslo
#define SYS_WEB_ACCESS sys[150]
#define WEB_ACCESS SYS_WEB_ACCESS

// 0..ethernet nefunguje, 1..ethernet OK
#define SYS_ETH_WORKS sys[24]
#define ETH_WORKS SYS_ETH_WORKS


// === trvala pamet ===
#define SYS_FLASH[n] sys[99 + (n)]
#define FLASH[n] SYS_FLASH[n]


// === GPIO D0 port ===

// Hodnoty D0 pinu (8 bitu)
#define SYS_D0  sys[301]
#define D0  SYS_D0

// Smer I/O D0 (1 out, 0 in)
#define SYS_D0_DIR  sys[302]
#define D0_DIR  SYS_D0_DIR


// === OPTO1 vstup ===

// hodnota 0 = ACTIVE
#define SYS_OPTO[n] sys[150 + (n)]
#define OPTO[n] SYS_OPTO[n]


// === nastaveni PWM ===

// PWM frekvence Hz
#define SYS_PWM_FREQ  sys[191]
#define PWM_FREQ  SYS_PWM_FREQ

// PWM strida (duty factor) - hodnota 0..FREQ
#define SYS_PWM_DUTY  sys[192]
#define PWM_DUTY  SYS_PWM_DUTY


// === cteni 1-WIRE teplomeru ===

// teplota je v C*100
#define SYS_TEMP[n] sys[309 + (n)]
#define TEMP[n] SYS_TEMP[n]


// === vystupy na rele ===
#define SYS_RELAY[n] sys[230 + (n)]
#define RELAY[n] SYS_RELAY[n]


// === cteni A/D ===

// namerene hodnoty

#define SYS_AD[n] sys[430 + (n)]
#define AD[n] SYS_AD[n]

// nastaveni na webovem rozhrani
// Pozor! offset je uz odecteny!

#define SYS_AD_OFFSET[n] sys[435 + 4 * (n - 1)]
#define SYS_AD_DIV[n]    sys[436 + 4 * (n - 1)]
#define SYS_AD_NAME[n]   sys[437 + 4 * (n - 1)]
#define SYS_AD_UNIT[n]   sys[438 + 4 * (n - 1)]

#define AD_OFFSET[n] SYS_AD_OFFSET[n]
#define AD_DIV[n]    SYS_AD_DIV[n]
#define AD_NAME[n]   SYS_AD_NAME[n]
#define AD_UNIT[n]   SYS_AD_UNIT[n]


// === mereni S0 ===

// tarif
// 0 ... T0 (vysoky),
// 1 ... T1 (nizky)
#define SYS_S0_TARIF  sys[459]
#define S0_TARIF  SYS_S0_TARIF

// nastaveni pomeru mericiho transformatoru MTD
#define SYS_S0_MTD[n]  sys[459 + (n)]
#define S0_MTD[n] SYS_S0_MTD[n]

// pocitadlo impulzu pro vysoky tarif T0
#define SYS_S0_T0[n]  sys[492 + (n)]
#define S0_T0[n] SYS_S0_T0[n]

// pocitadlo impulzu pro nizky tarif T1
#define SYS_S0_T1[n]  sys[525 + (n)]
#define S0_T1[n] SYS_S0_T1[n]

// pocet impulzu na jednotku, napr. 1 kWh (uziv. nastaveni)
#define SYS_S0_UNIT[n]  sys[558 + (n)]
#define S0_UNIT[n] SYS_S0_UNIT[n]

// delka mezery mezi impulzy (ms)
#define SYS_S0_WIDTH[n]  sys[591 + (n)]
#define S0_WIDTH[n] SYS_S0_WIDTH[n]

// jak dlouho od posledniho impulzu (ms)
#define SYS_S0_WIDTH_ACTUAL[n]  sys[624 + (n)]
#define S0_WIDTH_ACTUAL[n] SYS_S0_WIDTH_ACTUAL[n]

// end of include guard
#endif
