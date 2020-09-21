package com.ai.brain.controller;


import com.ai.brain.service.UserinfoService;
import com.ai.brain.vo.Userinfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("Userinfo")
public class UserinfoController {

    @Autowired
    private UserinfoService userinfoService;

    @GetMapping(value = "/{upk}")
    public ResponseEntity<Userinfo> getUserinfo(@PathVariable("upk") int upk) {
//        List<Userinfo> userinfo = userinfoService.findAllByUpk(1);
        System.out.println("ss");


            Optional<Userinfo> userinfo = userinfoService.findByUpk(upk);
            System.out.println(userinfo);
        System.out.println("ss");
        return new ResponseEntity<>(null, HttpStatus.OK);
    }

    @GetMapping("all")
    public ResponseEntity<List<Userinfo>> selectAll(){
        List<Userinfo> list = userinfoService.findAll();

        return new ResponseEntity<List<Userinfo>>(list,HttpStatus.OK);
    }

}
