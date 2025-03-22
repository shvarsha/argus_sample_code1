package com.persistent.aicrew.controller;

import com.persistent.aicrew.dao.entity.Underwriting;
import com.persistent.aicrew.service.UnderwritingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.CrossOrigin;

import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/sample")
public class UnderwritingController {
    @Autowired
    private UnderwritingService underwritingService;

    @RequestMapping(value = "/getAllUnderwriting", method = RequestMethod.GET)
    public ResponseEntity<List<Underwriting>> getUnderwritings() throws Exception {
        List<Underwriting> underwritingList = underwritingService.fetchAllunderwritings();
        return new ResponseEntity<List<Underwriting>>(underwritingList, HttpStatus.OK);
    }
}