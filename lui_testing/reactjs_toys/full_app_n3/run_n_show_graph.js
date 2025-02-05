'use client'
import Image from "next/image";

import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { useState } from 'react';

function MyPostButton({msgHere}) {
  const [response, setResponse] = useState(null);
  const handleClick = async () => {
    try {
      const res = await fetch("http://127.0.0.1:45678", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msgHere }),
      });
      const data = await res.json();
      setResponse(data);
      console.log("data =", data);
      alert(JSON.stringify(data));
    } catch (error) {
      console.error("Error:", error);
      setResponse({ error: "Failed to connect to the server." });
      console.log("res ERROR");
    }
  }
  return (
    <button onClick={handleClick}>
      Do POST
    </button>
  );
}

/*
def show_tree(step = None, curr = None, indent = 1):
    if( step.success == True ):
        stp_prn = " T "

    elif( step.success == False ):
        stp_prn = " F "

    else:
        stp_prn = " N "

    str_lin_num = "{:3}".format(step.lin_num)

    stp_prn += str_lin_num + "     " * indent + " └──"
    try:
        stp_prn += str(step.command)

    except:
        stp_prn += "None"

    if( step.lin_num == curr ):
        stp_prn += "            <<< here "

    print(stp_prn)
    try:
        for line in step.next_step_list:
            show_tree(step = line, curr = curr, indent = indent + 1)

    except:
        #print("last indent =", indent)
        pass
*/

//function show_tree(step, curr, indent = 1){

function show_tree(pos_num, my_lst, indent = 1){
    let step = my_lst[pos_num]
    //console.log("indent =", indent)
    let stp_prn = "";
    //console.log("step.success=", step.success);
    if( step.success === true ){
        let stp_prn = " T ";
    }
    else if( step.success === false ){
        let stp_prn = " F ";
    }
    else {
        let stp_prn = " N ";
    }
    //console.log("step.lin_num", step.lin_num)
    let str_lin_num = String(step.lin_num);
    //console.log("step.command", step.command)
    stp_prn = stp_prn + "      ".repeat(indent) + " └──";
    try{
        stp_prn = stp_prn + String(step.command)
    } catch (error) {
        stp_prn = stp_prn + "None"
    }
    /*if( step.lin_num === curr ):
        stp_prn = stp_prn + "            <<< here "*/

    console.log(stp_prn)
    try{
        for (let new_pos of step.nxt) {
            //show_tree(step = line, curr = curr, indent = indent + 1);
            show_tree(new_pos, my_lst, indent + 1);
        }

    } catch (error) {
        console.log("last indent =", indent);
    }

}
/*
[HMR] connected websocket.ts:32:21
Node: 0 comm: ['aaa'] prev: None nxt:   1 index.js:129:16
Node: 1 comm: ['bbb'] prev: 0 nxt:   2 index.js:129:16
Node: 2 comm: ['ccc'] prev: 1 nxt:   3 index.js:129:16
Node: 3 comm: ['xxxx'] prev: 2 nxt:   4 index.js:129:16
Node: 4 comm: ['ggggggg'] prev: 3 nxt:   5 index.js:129:16
Node: 5 comm: None prev: 4 nxt: empty                           <<< here I am <<< index.js:129:16
step.success= undefined index.js:71:12
step.lin_num undefined index.js:82:12
step.command undefined index.js:86:12
undefined0 └──undefined index.js:98:12
last indent = 1 index.js:106:16
my_lst =
Array(6) [ "0 comm: ['aaa'] prev: None nxt:   1", "1 comm: ['bbb'] prev: 0 nxt:   2", "2 comm: ['ccc'] prev: 1 nxt:   3", "3 comm: ['xxxx'] prev: 2 nxt:   4", "4 comm: ['ggggggg'] prev: 3 nxt:   5", "5 comm: None prev: 4 nxt: empty                           <<< here I am <<<" ]
index.js:134:14

*/


function MyGetButton({msgHere}) {
  const [response, setResponse] = useState(null);
  const handleClick = async () => {
    try {
      const path_in = new URLSearchParams({ msgHere }).toString();
      const res = await fetch(`http://127.0.0.1:45678?${path_in}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      const data = await res.json();
      setResponse(data);
      var my_lst = data.Answer;


      for (let i = 0; i < my_lst.length; i++) {
        console.log("Node:", my_lst[i]);
      }

      show_tree(0, my_lst, 1);

      console.log("my_lst =", my_lst);
      alert(JSON.stringify(my_lst));
    } catch (error) {
      console.error("Error <<", error, ">>");
      setResponse({ error: "Failed to connect to the server." });
      console.log("res ERROR");
    }
  }
  return (
    <button onClick={handleClick}>
      Do GET
    </button>
  );
}


export default function Home() {
  const [usrName, setName] = useState('');
  return (
    <div>
      <h2> Two http Buttons </h2>
      <label>
        Give name here:
        <input
          value={usrName}
          onChange={e => setName(e.target.value)}
        />
      </label>
      <MyPostButton msgHere ={usrName} />
      <MyGetButton msgHere ={usrName} />
    </div>
  );
}
