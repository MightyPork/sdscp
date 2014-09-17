#pragma once

// Dataflash read/write utils

// public API:

// _df_read(addr)
// _df_write(addr, value)
// _df_flush()

// index v ram[]
#ifndef DF_TMP_START
#define DF_TMP_START 200
#endif

// get dataflash page for address index
#define _get_df_page(i) ((i)/66)

var df_current_page = -1;
var df_page_dirty = false;


/* Open dataflash page the address is in */
_df_open_for_address(addr)
{
	var page = _get_df_page(addr);

	// no page change
	if(df_current_page == page) return;

	// save old page if dirty
	if(page != df_current_page) {
		_df_save_page();
	}

	// load new page
	echo("Opening DF page #", page, " for addr:", addr);
	read_dataflash_page_to_ram(page, DF_TMP_START);
	df_current_page = page;
	df_page_dirty = false;
}


/* Save open page if dirty */
_df_save_page()
{
	if(df_current_page != -1 && df_page_dirty) {
		echo("Saving open DF page: #", df_current_page);
		write_ram_block_to_dataflash_page(df_current_page, DF_TMP_START);
		df_page_dirty = false;
	}
}


/* alias for closing dataflash  */
#define _df_flush() _df_save_page()


/* write to dataflash, minimizing read/write cycle count */
_df_write(addr, value)
{
	_df_open_for_address(addr);

	var ram_addr = DF_TMP_START + (addr - (df_current_page * 66));

	if(ram[ram_addr] != value) {
		ram[ram_addr] = value;

		df_page_dirty = true;

		echo("DF[", addr, "] = ", value);
	}
}


/* Read from DF */
_df_read(addr)
{
	read_dataflash(addr);
	return _DATAFLASH_BUFFER;
}


/* inline read-to function (target is reference to target variable) */
#define _df_read_to(target, addr) {
	read_dataflash(addr);
	target = _DATAFLASH_BUFFER;
}



