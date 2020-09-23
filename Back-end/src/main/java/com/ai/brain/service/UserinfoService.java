package com.ai.brain.service;

import com.ai.brain.repository.UserinfoRepository;
import com.ai.brain.vo.UserIdPw;
import com.ai.brain.vo.Userinfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

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
        return userinfoRepository.findById(uPk);
    }

    // id 변경하기
    public Userinfo updateId(Userinfo userinfo, String newId){
        System.out.println("updateId Service");
        userinfo.setUId(newId);
        return userinfoRepository.save(userinfo);
    }

    // pw 변경하기
    public Userinfo updatePw(Userinfo userinfo, String newPw){
        System.out.println("updatePw Service");
        userinfo.setUPw(newPw);
        return userinfoRepository.save(userinfo);
    }

    // 회원 탈퇴
    public void deleteAccount(Userinfo userinfo){
        System.out.println("deleteAccount Service");

        userinfoRepository.deleteById(userinfo.getUPk());
    }

//    public List<Userinfo> findAll() {
//        List<Userinfo> list = userinfoRepository.findAll();
//        return list;
//    }
}
