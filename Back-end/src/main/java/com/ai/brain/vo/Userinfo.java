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

    private String uId;
    
    private String uPw;
    
    private String uName;

}
