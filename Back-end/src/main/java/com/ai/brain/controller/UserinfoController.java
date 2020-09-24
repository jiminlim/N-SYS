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
@CrossOrigin(origins = { "*" }, maxAge = 6000)
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
            map.put("Userinfo", userinfo);

            return new ResponseEntity<HashMap<String, Object>>(map, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }
    }

    @GetMapping(value = "/userinfo/{upk}")
    @ApiOperation(value = "회원 pk 로 회원 정보 가져오기")
    public ResponseEntity<HashMap<String, Object>> getUserinfo(@PathVariable("upk") int upk) {
        System.out.println("getUserinfo Controller");
        try {
            HashMap<String, Object> map = new HashMap<>();
            Optional<Userinfo> userinfo = userinfoService.getUserinfo(upk);
            map.put("Userinfo", userinfo.get());

            return new ResponseEntity<HashMap<String, Object>>(map, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }

    }

    @PutMapping(value = "/updateid/{Userinfo}/{newName}")
    @ApiOperation(value = "닉네임 변경하기")
    public ResponseEntity<HashMap<String, Object>> updateId(@PathVariable("Userinfo") Userinfo userinfo, @PathVariable("newName") String newName) {
        System.out.println("updateId Controller");
        try {
            HashMap<String, Object> map = new HashMap<>();
            userinfoService.updateId(userinfo, newName);
            map.put("Userinfo", userinfo);

            return new ResponseEntity<HashMap<String, Object>>(map, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }

    }

    @PutMapping(value = "/updatepw/{Userinfo}/{newPw}")
    @ApiOperation(value = "pw 변경하기")
    public ResponseEntity<HashMap<String, Object>> updatePw(@PathVariable("Userinfo") Userinfo userinfo, @PathVariable("newPw") String newPw) {
        System.out.println("updatePw Controller");
        try {
            HashMap<String, Object> map = new HashMap<>();
            userinfoService.updatePw(userinfo, newPw);
            map.put("Userinfo", userinfo);

            return new ResponseEntity<HashMap<String, Object>>(map, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }

    }

    @DeleteMapping("/deleteaccount")
    @ApiOperation(value = "회원 탈퇴")
    public ResponseEntity<HashMap<String, Object>> deleteAccount(@RequestBody Userinfo userinfo) {
        System.out.println("deleteAccount Controller");
        try {
            HashMap<String, Object> map = new HashMap<>();
            userinfoService.deleteAccount(userinfo);
            map.put("Userinfo", "deleted!");

            return new ResponseEntity<HashMap<String, Object>>(map, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }
    }

    @PostMapping("/login")
    @ApiOperation(value = "로그인")
    public ResponseEntity<HashMap<String, Object>> login(@RequestParam String loginId, @RequestParam String loginPw) {
        System.out.println("login Controller");
        try {
            HashMap<String, Object> map = new HashMap<>();
            boolean flag = userinfoService.login(loginId, loginPw);

            if (flag) {
                map.put("Userinfo", "succ");
            } else {
                map.put("Userinfo", "fail");
            }

            return new ResponseEntity<HashMap<String, Object>>(map, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }
    }

    @PostMapping("/logout")
    @ApiOperation(value = "로그아웃")
    public ResponseEntity<HashMap<String, Object>> logout() {
        System.out.println("logout Controller");
        try {
            HashMap<String, Object> map = new HashMap<>();

            map.put("logout", "1");

            return new ResponseEntity<HashMap<String, Object>>(map, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.NOT_FOUND);
        }
    }

}
