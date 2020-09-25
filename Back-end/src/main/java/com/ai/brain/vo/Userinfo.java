package com.ai.brain.vo;

import lombok.*;

import javax.persistence.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Entity
public class Userinfo {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int uPk;

    @Column(name="u_id")
    private String uiId;
    
    @Column(name="u_pw")
    private String uiPw;
    
    @Column(name="u_name")
    private String uiName;

}
