package com.persistent.aicrew.service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.persistent.aicrew.dao.entity.Bill;
import com.persistent.aicrew.repository.BillRepository;

@Service
public class BillService {

	@Autowired
	private BillRepository billRepository;

	public List<Bill> getBills() {
		List<Bill> result = new ArrayList<>();
		billRepository.findAll().forEach(result::add);
		return result;
	}

	/**
	 * 
	 * @param billID
	 * @return
	 */
	public List<Bill> getBills(Integer claimID) {
		return billRepository.findBillsByClaimID(claimID);
		// return
		// billRepository.findById(claimID).map(Collections::singletonList).orElseGet(Collections::emptyList);
	}

}
