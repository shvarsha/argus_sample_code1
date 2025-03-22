package com.persistent.aicrew.dao.entity;


import javax.persistence.*;
import java.sql.Date;

@Entity
@Table(name="Bill")
public class Bill {


    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "bill_id")
    private Integer bill_id;
    @Column(name = "bill_date")
    private Date bill_date;

    @Column(name = "bill_description")
    private String bill_description;


    @Column(name = "bill_amount")
    private Double bill_amount;

    @Column(name = "claim_id")
    private Integer claim_id;


    public Integer getBill_id() {
        return bill_id;
    }

    public void setBill_id(Integer bill_id) {
        this.bill_id = bill_id;
    }

    public Date getBill_date() {
        return bill_date;
    }

    public void setBill_date(Date bill_date) {
        this.bill_date = bill_date;
    }

    public String getBill_description() {
        return bill_description;
    }

    public void setBill_description(String bill_description) {
        this.bill_description = bill_description;
    }

    public Double getBill_amount() {
        return bill_amount;
    }

    public void setBill_amount(Double bill_amount) {
        this.bill_amount = bill_amount;
    }

    public Integer getClaim_id() {
        return claim_id;
    }

    public void setClaim_id(Integer claim_id) {
        this.claim_id = claim_id;
    }


}
