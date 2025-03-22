package com.persistent.aicrew.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.persistent.aicrew.dao.entity.Claim;
import com.persistent.aicrew.repository.ClaimsRepository;

@Service
public class ClaimService {

	@Autowired
	private ClaimsRepository claimsRepository;
	
	public List<Claim> fetchAllClaims() {
		List<Claim> result = new ArrayList<Claim>();
		claimsRepository.findAll().forEach(result::add);
		return result;
	}
	
}
