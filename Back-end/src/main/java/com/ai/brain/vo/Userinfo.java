package com.ai.brain.vo;

import lombok.*;
import javax.persistence.*;

@Getter
@NoArgsConstructor
@AllArgsConstructor
@Entity(name = "Userinfo")
public class Userinfo {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int uPk;

    private String uId;

    private String uPw;

}
