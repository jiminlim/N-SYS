package com.ai.brain.service;

import com.ai.brain.repository.UserinfoRepository;
import com.ai.brain.vo.Userinfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.swing.text.html.Option;
import java.util.List;
import java.util.Optional;

@Service
public class UserinfoService {

    @Autowired
    private UserinfoRepository userinfoRepository;

    public Optional<Userinfo> findByUpk(int uPk){
        Optional<Userinfo> userinfo = userinfoRepository.findById(uPk);
        return userinfo;
    }

    public List<Userinfo> findAll() {
        List<Userinfo> list = userinfoRepository.findAll();
        return list;
    }
}
