package com.persistent.aicrew.repository;

import org.springframework.data.repository.CrudRepository;

import com.persistent.aicrew.dao.entity.Claim;

public interface ClaimsRepository extends CrudRepository<Claim, Integer>{
	
}
