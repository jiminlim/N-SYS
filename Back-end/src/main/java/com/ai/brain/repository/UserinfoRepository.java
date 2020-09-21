package com.ai.brain.repository;

import com.ai.brain.vo.Userinfo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserinfoRepository extends JpaRepository<Userinfo, Integer> {

//    public Userinfo findByUPk(int uPk);
//    public List<Userinfo> findByUpk(int num);
//    public Userinfo findByUpk(int num);

}
