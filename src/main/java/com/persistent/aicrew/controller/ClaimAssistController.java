package com.persistent.aicrew.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.CrossOrigin;
import com.persistent.aicrew.dao.entity.Claim;
import com.persistent.aicrew.service.ClaimService;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/sample")
public class ClaimAssistController {

	@Autowired
	private ClaimService claimService;
	
    @RequestMapping("/") 
    public String hello() {
        return "Hello World!";
    }
    
	@RequestMapping(value="/getAllClaims",method = RequestMethod.GET)
	public ResponseEntity<List <Claim>> getClaims(){
		List <Claim> claimList = claimService.fetchAllClaims();
		return new ResponseEntity<List <Claim>>(claimList, HttpStatus.OK);
	}
}
