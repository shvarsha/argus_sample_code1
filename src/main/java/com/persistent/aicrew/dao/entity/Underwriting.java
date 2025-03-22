package com.persistent.aicrew.dao.entity;

import javax.persistence.*;

@Entity
@Table(name="Underwriting")
public class Underwriting {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Integer id;

    @Column(name = "age")
    private Integer age;

    @Column(name = "gender")
    private String gender;

    @Column(name = "bmi")
    private Long bmi;

    @Column(name = "occupation")
    private String occupation;

    @Column(name = "medical_history")
    private String medicalHistory;

    @Column(name = "risk_meter")
    private String riskMeter;

    @Column(name = "rate_meter")
    private Long rateMeter;

    @Column(name = "approved")
    private boolean approved;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public Long getBmi() {
        return bmi;
    }

    public void setBmi(Long bmi) {
        this.bmi = bmi;
    }

    public String getOccupation() {
        return occupation;
    }

    public void setOccupation(String occupation) {
        this.occupation = occupation;
    }

    public String getMedicalHistory() {
        return medicalHistory;
    }

    public void setMedicalHistory(String medicalHistory) {
        this.medicalHistory = medicalHistory;
    }

    public String getRiskMeter() {
        return riskMeter;
    }

    public void setRiskMeter(String riskMeter) {
        this.riskMeter = riskMeter;
    }

    public Long getRateMeter() {
        return rateMeter;
    }

    public void setRateMeter(Long rateMeter) {
        this.rateMeter = rateMeter;
    }

    public boolean getApproved() {
        return approved;
    }

    public void setApproved(boolean approved) {
        this.approved = approved;
    }
}
