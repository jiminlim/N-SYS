package com.ai.brain.service;

import com.ai.brain.repository.UserinfoRepository;
import com.ai.brain.vo.UserIdPw;
import com.ai.brain.vo.Userinfo;
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
        userinfo.setUName((userIdPw.getUName()));

        return userinfoRepository.save(userinfo);
    }

    // pk 로 회원 정보 가져오기
    public Optional<Userinfo> getUserinfo(int uPk) {
        System.out.println("getUserinfo Service");
        return userinfoRepository.findById(uPk);
    }

    // 닉네임 변경하기
    public Userinfo updateId(Userinfo userinfo, String newName) {
        System.out.println("updateId Service");
        userinfo.setUName(newName);
        return userinfoRepository.save(userinfo);
    }

    // pw 변경하기
    public Userinfo updatePw(Userinfo userinfo, String newPw) {
        System.out.println("updatePw Service");
        userinfo.setUPw(newPw);
        return userinfoRepository.save(userinfo);
    }

    // 회원 탈퇴
    public void deleteAccount(Userinfo userinfo) {
        System.out.println("deleteAccount Service");

        userinfoRepository.deleteById(userinfo.getUPk());
    }

    // 로그인
    public boolean login(String loginId, String loginPw) {
        System.out.println("login Service");

        List<Userinfo> list = userinfoRepository.findAll();

        // id 확인
        boolean flag = false;
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).getUId().equals(loginId)) {
                // pw 확인
                if (list.get(i).getUPw().equals(loginPw)) {
                    flag = true;
                } else {
                    flag = false;
                }
                break;
            }
        }

        return flag;
    }

    // 로그아웃
    public void logout() {

    }

//    public List<Userinfo> findAll() {
//        List<Userinfo> list = userinfoRepository.findAll();
//        return list;
//    }
}
