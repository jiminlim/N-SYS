package com.ai.brain.controller;

import com.ai.brain.service.UserinfoService;
import com.ai.brain.vo.UserIdPw;
import com.ai.brain.vo.Userinfo;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;

@RestController
@RequestMapping("Userinfo")
public class UserinfoController {

    @Autowired
    private UserinfoService userinfoService;

    // 회원 가입
    @PostMapping("/join")
    @ApiOperation(value = "회원 가입")
    public ResponseEntity<HashMap<String, Object>> join(@RequestBody UserIdPw userIdPw) {
        System.out.println("join Controller");
        try {
            HashMap<String, Object> map = new HashMap<>();
            Userinfo userinfo = userinfoService.join(userIdPw);
            map.put("Userinfo", userinfo.toString());
            return new ResponseEntity<HashMap<String, Object>>(map, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }
    }

//
//    @GetMapping(value = "/{upk}")
//    public ResponseEntity<Userinfo> getUserinfo(@PathVariable("upk") int upk) {
////        List<Userinfo> userinfo = userinfoService.findAllByUpk(1);
//        System.out.println("ss");
//
//        Userinfo userinfo = userinfoService.findByUpk(upk);
//        System.out.println(userinfo);
//        System.out.println(userinfo);
//        System.out.println("ss");
//        return new ResponseEntity<>(null, HttpStatus.OK);
//    }
//
//    // 전체 회원 정보 출력
//    @GetMapping("all")
//    public ResponseEntity<List<Userinfo>> selectAll() {
//        List<Userinfo> list = userinfoService.findAll();
//
//        return new ResponseEntity<List<Userinfo>>(list, HttpStatus.OK);
//    }


    // PK로 회원 불러오기
//    @GetMapping("/{upk}")


    // 회원 id 수정


    // 회원 삭제

}
