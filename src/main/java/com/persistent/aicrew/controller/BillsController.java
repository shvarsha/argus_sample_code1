package com.persistent.aicrew.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.persistent.aicrew.dao.entity.Bill;
import com.persistent.aicrew.service.BillService;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/sample")
public class BillsController {

	@Autowired
	private BillService billService;

	/*
	 * @RequestMapping(value="/saveBill",method = RequestMethod.GET) public String
	 * saveBill() throws ParseException { SimpleDateFormat formatter = new
	 * SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH);
	 * 
	 * 
	 * //Date date = formatter.parse(dateInString); for ( BillDataEnum
	 * billEnum:BillDataEnum.values()) { Bill bill = new Bill();
	 * bill.setClaim_id(billEnum.getClaimid());
	 * bill.setBill_id(billEnum.getBillid());
	 * System.out.println(billEnum.getBillDate());
	 * 
	 * bill.setBill_date(new
	 * java.sql.Date((formatter.parse(billEnum.getBillDate())).getTime()));
	 * bill.setBill_description(billEnum.getBillDescr());
	 * bill.setBill_amount(billEnum.getAmt()); claimService.saveBill(bill); } return
	 * "Bill Data added successfully."; }
	 */

	@RequestMapping(value = "/getAllBills", method = RequestMethod.GET)
	public ResponseEntity<List<Bill>> getBills() {
		List<Bill> billList = billService.getBills();
		return new ResponseEntity<List<Bill>>(billList, HttpStatus.OK);
	}

	@RequestMapping(value = "/claims/{claimID}", method = RequestMethod.GET)
	public ResponseEntity<List<Bill>> getClaimBills(@PathVariable Integer claimID) {
		return new ResponseEntity<>(billService.getBills(claimID), HttpStatus.OK);
	}

}
