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
import java.util.Optional;

@RestController
@RequestMapping("Userinfo")
public class UserinfoController {

    @Autowired
    private UserinfoService userinfoService;

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

    @GetMapping(value = "/{upk}")
    @ApiOperation(value = "회원 pk 로 회원 정보 가져오기")
    public ResponseEntity<HashMap<String, Object>> getUserinfo(@PathVariable("upk") int upk) {
        System.out.println("getUserinfo Controller");
        try {
            HashMap<String, Object> map = new HashMap<>();
            Optional<Userinfo> userinfo = userinfoService.getUserinfo(upk);
            map.put("Userinfo", userinfo.get().toString());
            return new ResponseEntity<HashMap<String, Object>>(map, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }

    }

    // 회원 id 수정


    // 회원 삭제

}
