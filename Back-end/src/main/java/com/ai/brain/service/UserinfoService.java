package com.ai.brain.service;

import com.ai.brain.repository.UserinfoRepository;
import com.ai.brain.vo.UserIdPw;
import com.ai.brain.vo.Userinfo;
import org.apache.catalina.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserinfoService {

    @Autowired
    private UserinfoRepository userinfoRepository;


    // 회원 가입
    public Userinfo join(UserIdPw userIdPw) {
        System.out.println("join Service");
        Userinfo userinfo = new Userinfo();
        userinfo.setUId(userIdPw.getUId());
        userinfo.setUPw(userIdPw.getUPw());

        return  userinfoRepository.save(userinfo);
    }

    // pk 로 회원 정보 가져오기
    public Optional<Userinfo> getUserinfo(int uPk) {
        System.out.println("getUserinfo Service");
        Userinfo userinfo = new Userinfo();
        userinfo.setUPk(uPk);
        userinfoRepository.findById(uPk);

        return userinfoRepository.findById(uPk);
    }

    public List<Userinfo> findAll() {
        List<Userinfo> list = userinfoRepository.findAll();
        return list;
    }
}
