*** Settings ***
Library         SeleniumUtil
Library         poms.HomePage
Library         pcap.Pcap
Library         poms.LoginPage

Test Setup      Start Sniffing
Test Teardown   close browser


*** Variables ***
${host}                 kissanime.ru
${url}                  http://${host}
${uri}                  /Login
${user}                 johndoe111405
${pass}                 Fall#n14


*** Test Cases ***
Login To Kissanime
    login as user
    insert user name    ${user}
    insert password     ${pass}
    sign in
#    &{cred} =           sign in
#    should be equal     &{cred}[username]  ${user}
#    should be equal     &{cred}[password]  ${pass}


*** keywords ***
Start Sniffing
    sniff               ${host}     ${uri}
    open browser        ${url}



