package com.persistent.aicrew.repository;

import java.util.List;

import javax.persistence.EntityManager;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.repository.CrudRepository;

import com.persistent.aicrew.dao.entity.Bill;

public interface BillRepository extends CrudRepository<Bill, Integer>,BillRepositoryCustom {

}

interface BillRepositoryCustom {
	List<Bill> findBillsByClaimID(Integer claimID);
}

class BillRepositoryImpl implements BillRepositoryCustom {

	@Autowired
	private EntityManager entityManager;

	/**
	 * 
	 */
	@Override
	public List<Bill> findBillsByClaimID(Integer claimID) {
		String jpql = "select b from Bill b where claim_id = :claimID";
		javax.persistence.Query q = entityManager.createQuery(jpql);
		q.setParameter("claimID", claimID);
		return (List<Bill>) q.getResultList();
	}

}
