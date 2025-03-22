package com.persistent.aicrew.service;

import com.persistent.aicrew.dao.entity.Underwriting;
import com.persistent.aicrew.repository.UnderwritingsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class UnderwritingService {
    @Autowired
    private UnderwritingsRepository underwritingsRepository;

    public List<Underwriting> fetchAllunderwritings() throws Exception {
        List<Underwriting> result = new ArrayList<Underwriting>();
        underwritingsRepository.findAll().forEach(result::add);;

        return result;
    }
}
