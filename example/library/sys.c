#pragma once
#pragma renderer sds2

// -------------------------- SYSTEM MACROS -----------------------------

// Reference
// - funkce ..... http://wiki.merenienergie.cz/index.php/Sdsc_sysf
// - promenne ... http://wiki.merenienergie.cz/index.php/Sdsc_sysp

#define true 1
#define false 0

// ########## Aliasy systemovych promennych ##########

#define TEXT_END 512
#define RAM_END 512
#define SYS_END 1024


// uptime (v 10ms)
#define _UPTIME sys[3]

// unix timestamp NTP
#define _TIMESTAMP sys[4]
#define _NTP_STATUS sys[37]

#define _TIME_DAY sys[5]
#define _TIME_MONTH sys[6]
#define _TIME_YEAR sys[7]
#define _TIME_H sys[8]
#define _TIME_M sys[9]
#define _TIME_S sys[10]

// rychlost, 0..1 krok/ms, 128..max rychlost
#define _SPEED sys[63]
#define N_SPEED_NORMAL 0
#define N_SPEED_FULL 128

// odpočet sekund, každou sekundu se sníží o 1
#define _TIMER sys[64]


#define _OSI7_STATUS sys[65]
#define N_OSI7_BUSY 0

#define N_NET_FAILED 128	// Ethernet disconnected during OSI7

// SMPT
#define N_SMTP_BUSY					0
#define N_SMTP_OK 					256 // Success
#define N_SMTP_FAIL_TIMEOUT 		257	// SMTP TIMEOUT
#define N_SMTP_FAIL_NOT_READY 		258	// SMTP server není přípraven (not ready)
#define N_SMTP_FAIL_BAD_HELO 		259	// Chyba v HELO příkazu.
#define N_SMTP_FAIL_BAD_SENDER 		260 // Neplatná adresa odesílatele.
#define N_SMTP_FAIL_BAD_RECIPIENT 	261	// Neplatná adresa příjemce.
#define N_SMTP_FAIL_ACCESS_DENIED 	262	// RELAY ACCESS DENIED
#define N_SMTP_FAIL_BAD_BODY 		263	// Nelze odeslat data (obsah emailu).
#define N_SMTP_FAIL_CANNOT_COMPLETE	264	// Nelze dokončit odesílání dat.
#define N_SMTP_FAIL_AUTH_DISABLED	265	// Autentifikace není povolena na tomto SMTP serveru.
#define N_SMTP_FAIL_BAD_USER		266	// Neplatné uživatelské jméno.
#define N_SMTP_FAIL_BAD_PASSWORD	267	// Neplatné uživatelské heslo.
#define N_SMTP_FAIL_INVALID_RECIPIENT 268 // Chyba 550 Invalid recipient (často spam filter)
#define N_SMTP_FAIL_NO_CONNECT		269	// Nelze navázat TCP spojení na SMTP server (neplatná IP, server mimo provoz)
#define N_SMTP_NOT_READY			270	// Právě probíhá odesílání emailu (pokud chcete poslat další email dříve než je odeslán aktuální).
#define N_SMTP_FAIL_NOT_COMPATIBLE	271	// SMTP server vrátil chybu 501 (nekompatibilita mezi SMTP serverem a klientem)
#define N_SMTP_FAIL_OUT_OF_MEMORY	272	// Nedostatek paměti v zařízení SDS pro odeslání emailu (tato chyba by se nikdy neměla stát)
#define N_SMTP_FAIL_BAD_IP			273	// IP adresa zařízení SDS není platná (obvykle DHCP problém), nelze tedy zahájit komunikaci
#define _SMTP_IP[n] sys[80+n] //one-based
#define _SMTP_STATUS _OSI7_STATUS

// DNS RESOLV
#define _DNS_STATUS _OSI7_STATUS
#define _DNS_RESOLVER_IP[n] sys[69+(n)] // one-based
#define _DNS_RESULT_IP[n] sys[65+(n)] // one-based
#define N_DNS_BUSY	0
#define N_DNS_OK 	512		// resolv proběhl OK
#define N_DNS_FAIL	513		// resolv hlásí chybu
#define N_DNS_WAITING 514	// resolv odeslal požadavek na server a čeká na odpověď

// HTTP
#define _HTTP_PORT sys[76]  // default 80 - port pro http_get

#define _HTTP_STORE_MODE sys[77]  // 0..discard, 1..ram[], 2..text[]
#define N_HTTP_STORE_NONE 0
#define N_HTTP_STORE_RAM 1
#define N_HTTP_STORE_TEXT 2
#define _HTTP_STORE_LENGTH sys[78]  // number of chars to receive
#define _HTTP_RESPONSE_LENGTH ram[0]  // number of bytes received from http_get
#define _HTTP_CODE sys[75]  // 200, 404...
#define _HTTP_STATUS _OSI7_STATUS
#define N_HTTP_BUSY	0
#define N_HTTP_OK 					1024 // HTTP GET proběhl OK, webový server poslal odpověď - hodnota odpovědi je v sys[75]
#define N_HTTP_FAIL_NO_CONNECT 		1025 // chyba - nelze vytvořit připojení
#define N_HTTP_FAIL_TIMEOUT 		1026 // chyba - timeout (neobdržel jakokoliv odpověď do stanoveného času) (různé důvody, typicky výpadek připojení nebo serveru)
#define N_HTTP_FAIL_CONNECTION_RESET 1027 // chyba - odpojeno - webový server násilně přerušil síťové spojení (reset)
#define N_HTTP_FAIL_BAD_RESPONSE 	1028 // chyba - přijaty nesmyslné data (méně než 12 znaků nebo neplatná hlavička)
#define N_HTTP_FAIL_NOT_READY 		1029 // chyba - stále není vyřízený předchozí požadavek, tento tedy je zahozen
#define N_HTTP_FAIL_BAD_IP 			1030 // chyba - IP adresa zařízení SDS není platná (obvykle DHCP problém), nelze tedy zahájit komunikaci

// PING
#define _PING_STATUS sys[92]
#define N_PING_READY 0
#define N_PING_PREPARING 1
#define N_PING_WAITING_ARP 2
#define N_PING_WAITING_ECHO 3
#define N_PING_OK 4
#define _PING_SEQ sys[93]
#define _PING_RTT sys[94]

// UDP
#define _UDP_STATUS sys[95]
#define N_UDP_READY 0
#define N_UDP_BUSY 1
#define N_UDP_SENT 2
#define N_UDP_SENT_ARP 3
#define N_UDP_FAIL_NOT_READY 4
#define N_UDP_FAIL_BAD_ARGS 5

// TRAP
#define _TRAP_STATUS sys[96]
#define N_TRAP_READY 0
#define N_TRAP_BUSY 1
#define N_TRAP_OK 2
#define N_TRAP_FAIL_BAD_ARGS 3
#define N_TRAP_FAIL_NO_ARP 4
#define N_TRAP_FAIL_NOT_READY 5


#define _RANDOM sys[61]
#define _ATOI_RESULT sys[62]
#define _SPRINTF_END sys[98]

// === uživatelské proměnné ===
#define _VAR[n] sys[139 + (n)] // one-based

// 0..control bez hesla, 1..pozadovat heslo
#define _WEB_ACCESS sys[150]
#define N_WEB_ACCESS_PUBLIC 0
#define N_WEB_ACCESS_PASSWORD 1

// 0..ethernet nefunguje, 1..ethernet OK
#define _ETH_WORKS sys[24]


// === trvalá paměť ===
// result of read/input of write to DF
#define _DATAFLASH_BUFFER sys[99]

#define _FLASH[n] sys[99 + (n)] // one-based


// === GPIO D0 port ===

// Hodnoty D0 pinu (8 bitu)
#define _D0  sys[301]

// Směr I/O D0 (1 out, 0 in)
#define _D0_DIR  sys[302]
#define N_D0_OUT 1
#define N_D0_IN 0


// === OPTO1 vstup ===

// hodnota 0 = ACTIVE
#define _OPTO[n] sys[150 + (n)] // one-based
#define N_OPTO_ACTIVE 0


// === nastavení PWM ===

// PWM frekvence Hz
#define _PWM_FREQ  sys[191]

// PWM střída (duty factor) - hodnota 0..FREQ
#define _PWM_DUTY  sys[192]


// === čtení 1-WIRE teploměru ===

// teplota je v C*100
#define _TEMP[n] sys[309 + (n)] // one-based
#define _TEMP_STATUS[n] sys[349 + (n)] // one-based
#define _TEMP_ROM[n] sys[899 + (n)] // one-based
#define _TEMP_NAME[n] sys[390 + (n)] // one-based
#define N_TEMP_ERROR 16777216 // hodnota teploty pokud teploměr chybí


// === vystupy na rele ===
#define _RELAY_ACCESS[n] sys[195 + (n)] // one-based
#define _RELAY[n] sys[230 + (n)] // one-based
#define _RELAY_NAME[n] sys[265 + (n)] // one-based


// === čtení A/D ===

// naměřené hodnoty

#define _AD[n] sys[430 + (n)]

// nastavení na webovem rozhrani
// Pozor! offset je uz odecteny!

#define _AD_OFFSET[n] sys[435 + 4 * (n - 1)] // one-based
#define _AD_DIV[n]    sys[436 + 4 * (n - 1)] // one-based
#define _AD_NAME[n]   sys[437 + 4 * (n - 1)] // one-based
#define _AD_UNIT[n]   sys[438 + 4 * (n - 1)] // one-based

// === mereni S0 ===

// tarif
// 0 ... T0 (vysoký),
// 1 ... T1 (nízký)
#define _S0_TARIF  sys[459]

// nastavení poměru měřícího transformátoru MTD
#define _S0_MTD[n]  sys[459 + (n)] // one-based

// počítadlo impulzů pro vysoký tarif T0
#define _S0_T0[n]  sys[492 + (n)] // one-based

// počítadlo impulzů pro nízký tarif T1
#define _S0_T1[n]  sys[525 + (n)] // one-based

// počet impulzů na jednotku, napr. 1 kWh (uživ. nastavení)
#define _S0_UNIT[n]  sys[558 + (n)] // one-based

// délka mezery mezi impulzy (ms)
#define _S0_WIDTH[n]  sys[591 + (n)] // one-based

// jak dlouho od posledního impulzu (ms)
#define _S0_WIDTH_ACTUAL[n]  sys[624 + (n)] // one-based
