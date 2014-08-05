#ifndef SYS_C_INCLUDED
#define SYS_C_INCLUDED

// -------------------------- SYSTEM MACROS -----------------------------

// Reference
// - funkce ..... http://wiki.merenienergie.cz/index.php/Sdsc_sysf
// - promenne ... http://wiki.merenienergie.cz/index.php/Sdsc_sysp


// ########## Aliasy systemovych promennych ##########

// Cislovane promenne SYS_NECO_1, SYS_NECO_2
// Index JEDNA PRED!!! prvni polozkou: __SYS_NECO
// Pak prvni NECO: sys[ __SYS_NECO + 1 ]


// uptime (v 10ms)
#define SYS_UPTIME sys[3]

// unix timestamp NTP
#define SYS_TIMESTAMP sys[4]

#define SYS_TIME_DAY sys[5]
#define SYS_TIME_MONTH sys[6]
#define SYS_TIME_YEAR sys[7]
#define SYS_TIME_H sys[8]
#define SYS_TIME_M sys[9]
#define SYS_TIME_S sys[10]

// rychlost, 0..1 krok/ms, 128..max rychlost
#define SYS_SPEED sys[63]


// odpocet sekund, kazkou sekundu se snizi do 0
#define SYS_TIMER sys[64]

// Wait for SYS_TIMER == 0
wait_for_timer()
{
	// do
wft_loop1:

	// while...
	if (SYS_TIMER != 0) goto wft_loop1;
}


#define SYS_OSI7_STATUS sys[65]
#define OSI7_STATUS_INTERRUPTED 128

#define SMTP_STATUS_OK 256


// Wait for http_get()
wait_for_http_get()
{
	echo("Waiting for get.");

	// do
wfhg_loop1:
	wait(1);
	// while...
	if (SYS_OSI7_STATUS == 0) goto wfhg_loop1;
}

#define SYS_HTTP_GET_RESULT sys[75]

#define HTTP_GET_RESULT() SYS_HTTP_GET_RESULT
#define HTTP_GET_STATUS() SYS_OSI7_STATUS

#define HTTP_GET_STATUS_OK 1024 // success

#define HTTP_GET_OK() (HTTP_GET_STATUS() == HTTP_GET_STATUS_OK) && (HTTP_GET_RESULT() == 200)



// === uzivatelske promenne ===

#define __SYS_VAR 139
#define __SYS_VAR_COUNT 10
#define SYS_VAR_1 sys[140]
#define SYS_VAR_2 sys[141]
#define SYS_VAR_3 sys[142]
#define SYS_VAR_4 sys[143]
#define SYS_VAR_5 sys[144]
#define SYS_VAR_6 sys[145]
#define SYS_VAR_7 sys[146]
#define SYS_VAR_8 sys[147]
#define SYS_VAR_9 sys[148]
#define SYS_VAR_10 sys[149]


// 0..control bez hesla, 1..pozadovat heslo
#define SYS_WEB_ACCESS sys[150]

// 0..ethernet nefunguje, 1..ethernet OK
#define SYS_ETH_WORKS sys[24]


// === trvala pamet ===

#define __SYS_FLASH 99
#define __SYS_FLASH_COUNT 16
#define SYS_FLASH_1 sys[100]
#define SYS_FLASH_2 sys[101]
#define SYS_FLASH_3 sys[102]
#define SYS_FLASH_4 sys[103]
#define SYS_FLASH_5 sys[104]
#define SYS_FLASH_6 sys[105]
#define SYS_FLASH_7 sys[106]
#define SYS_FLASH_8 sys[107]
#define SYS_FLASH_9 sys[108]
#define SYS_FLASH_10 sys[109]
#define SYS_FLASH_11 sys[110]
#define SYS_FLASH_12 sys[111]
#define SYS_FLASH_13 sys[112]
#define SYS_FLASH_14 sys[113]
#define SYS_FLASH_15 sys[114]
#define SYS_FLASH_16 sys[115]


// === GPIO D0 port ===

// Hodnoty D0 pinu (8 bitu)
#define SYS_D0  sys[301]

// Smer I/O D0 (1 out, 0 in)
#define SYS_D0_DIR  sys[302]


// === OPTO1 vstup ===

// hodnota 0 = ACTIVE

#define __SYS_OPTO 150
#define __SYS_OPTO_COUNT 8
#define SYS_OPTO_1 sys[151]
#define SYS_OPTO_2 sys[152]
#define SYS_OPTO_3 sys[153]
#define SYS_OPTO_4 sys[154]
#define SYS_OPTO_5 sys[155]
#define SYS_OPTO_6 sys[156]
#define SYS_OPTO_7 sys[157]
#define SYS_OPTO_8 sys[158]


// === nastaveni PWM ===

// PWM frekvence Hz
#define SYS_PWM_FREQ  sys[191]
// PWM strida (duty factor) - hodnota 0..FREQ
#define SYS_PWM_DUTY  sys[192]


// === cteni 1-WIRE teplomeru ===

// teplota je v C*100

#define __SYS_TEMP 309
#define __SYS_TEMP 32
#define SYS_TEMP_1   sys[310]
#define SYS_TEMP_2   sys[311]
#define SYS_TEMP_3   sys[312]
#define SYS_TEMP_4   sys[313]
#define SYS_TEMP_5   sys[314]
#define SYS_TEMP_6   sys[315]
#define SYS_TEMP_7   sys[316]
#define SYS_TEMP_8   sys[317]
#define SYS_TEMP_9   sys[318]
#define SYS_TEMP_10  sys[319]
#define SYS_TEMP_11  sys[320]
#define SYS_TEMP_12  sys[321]
#define SYS_TEMP_13  sys[322]
#define SYS_TEMP_14  sys[323]
#define SYS_TEMP_15  sys[324]
#define SYS_TEMP_16  sys[325]

#define SYS_TEMP_17  sys[326]
#define SYS_TEMP_18  sys[327]
#define SYS_TEMP_19  sys[328]
#define SYS_TEMP_20  sys[329]
#define SYS_TEMP_21  sys[330]
#define SYS_TEMP_22  sys[331]
#define SYS_TEMP_23  sys[332]
#define SYS_TEMP_24  sys[333]
#define SYS_TEMP_25  sys[334]
#define SYS_TEMP_26  sys[335]
#define SYS_TEMP_27  sys[336]
#define SYS_TEMP_28  sys[337]
#define SYS_TEMP_29  sys[338]
#define SYS_TEMP_30  sys[339]
#define SYS_TEMP_31  sys[340]
#define SYS_TEMP_32  sys[341]


// === vystupy na rele ===

#define __SYS_RELAY 230
#define __SYS_RELAY_COUNT 6
#define SYS_RELAY_1  sys[231]
#define SYS_RELAY_2  sys[232]
#define SYS_RELAY_3  sys[233]
#define SYS_RELAY_4  sys[234]
#define SYS_RELAY_5  sys[235]
#define SYS_RELAY_6  sys[236]


// === cteni A/D ===

// namerene hodnoty

#define __SYS_AD 430
#define __SYS_AD_COUNT 4
#define SYS_AD_1  sys[431]
#define SYS_AD_2  sys[432]
#define SYS_AD_3  sys[433]
#define SYS_AD_4  sys[434]

// nastaveni na webovem rozhrani
// Pozor! offset je uz odecteny!

#define SYS_AD_1_OFFSET sys[435]
#define SYS_AD_1_DIV    sys[436]
#define SYS_AD_1_NAME   sys[437]
#define SYS_AD_1_UNIT   sys[438]

#define SYS_AD_2_OFFSET sys[439]
#define SYS_AD_2_DIV    sys[440]
#define SYS_AD_2_NAME   sys[441]
#define SYS_AD_2_UNIT   sys[442]

#define SYS_AD_3_OFFSET sys[443]
#define SYS_AD_3_DIV    sys[444]
#define SYS_AD_3_NAME   sys[445]
#define SYS_AD_3_UNIT   sys[446]

#define SYS_AD_4_OFFSET sys[447]
#define SYS_AD_4_DIV    sys[448]
#define SYS_AD_4_NAME   sys[449]
#define SYS_AD_4_UNIT   sys[450]


// === mereni S0 ===

// tarif
// 0 ... T0 (vysoky),
// 1 ... T1 (nizky)
#define SYS_S0_TARIF  sys[459]

#define __SYS_S0_COUNT  8

// nastaveni pomeru mericiho transformatoru MTD
#define __SYS_S0_MTD  459
#define SYS_S0_MTD_1  sys[460]
#define SYS_S0_MTD_2  sys[461]
#define SYS_S0_MTD_3  sys[462]
#define SYS_S0_MTD_4  sys[463]
#define SYS_S0_MTD_5  sys[464]
#define SYS_S0_MTD_6  sys[465]
#define SYS_S0_MTD_7  sys[466]
#define SYS_S0_MTD_8  sys[467]

// pocitadlo impulzu pro vysoky tarif T0
#define __SYS_S0_T0  492
#define SYS_S0_T0_1  sys[493]
#define SYS_S0_T0_2  sys[494]
#define SYS_S0_T0_3  sys[495]
#define SYS_S0_T0_4  sys[496]
#define SYS_S0_T0_5  sys[497]
#define SYS_S0_T0_6  sys[498]
#define SYS_S0_T0_7  sys[499]
#define SYS_S0_T0_8  sys[500]

// pocitadlo impulzu pro nizky tarif T1
#define __SYS_S0_T1  525
#define SYS_S0_T1_1  sys[526]
#define SYS_S0_T1_2  sys[527]
#define SYS_S0_T1_3  sys[528]
#define SYS_S0_T1_4  sys[529]
#define SYS_S0_T1_5  sys[530]
#define SYS_S0_T1_6  sys[531]
#define SYS_S0_T1_7  sys[532]
#define SYS_S0_T1_8  sys[533]

// pocet impulzu na jednotku, napr. 1 kWh (uziv. nastaveni)
#define __SYS_S0_UNIT  558
#define SYS_S0_UNIT_1  sys[559]
#define SYS_S0_UNIT_2  sys[560]
#define SYS_S0_UNIT_3  sys[561]
#define SYS_S0_UNIT_4  sys[562]
#define SYS_S0_UNIT_5  sys[563]
#define SYS_S0_UNIT_6  sys[564]
#define SYS_S0_UNIT_7  sys[565]
#define SYS_S0_UNIT_8  sys[566]

// delka mezery mezi impulzy (ms)
#define __SYS_S0_GAP  591
#define SYS_S0_GAP_1  sys[592]
#define SYS_S0_GAP_2  sys[593]
#define SYS_S0_GAP_3  sys[594]
#define SYS_S0_GAP_4  sys[595]
#define SYS_S0_GAP_5  sys[596]
#define SYS_S0_GAP_6  sys[597]
#define SYS_S0_GAP_7  sys[598]
#define SYS_S0_GAP_8  sys[599]

// jak dlouho od posledniho impulzu (ms)
#define __SYS_S0_LAST  624
#define SYS_S0_LAST_1  sys[625]
#define SYS_S0_LAST_2  sys[626]
#define SYS_S0_LAST_3  sys[627]
#define SYS_S0_LAST_4  sys[628]
#define SYS_S0_LAST_5  sys[629]
#define SYS_S0_LAST_6  sys[630]
#define SYS_S0_LAST_7  sys[631]
#define SYS_S0_LAST_8  sys[632]

#endif
