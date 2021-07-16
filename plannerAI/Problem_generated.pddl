(define (problem SMSProblem)

    (:domain SMSDomainFile)
    
    (:objects 
		 PPLLOGISTICS1 - logistics
		 PPQQUALITY1 - quality
		 PPMMAINTENANCE1 - maintainence
		 ETB0100 - testbentch
		 SES0100 - esdProtection
		 ECB0100 - convyor
		 SST0100 - solderingTemp
		 SPS0100 - pressure
		 AHA0100 - humidityAcutator
		 EOS0100 - oscilloscope
		 SHS0100 - humitdity
		 ARA0100 - tempActuator
		 SRT0100 - roomTemp
		 SIR0100 - InfraRed

    )
    
    (:init   
		(isDateNear ETB0100)
		(isBadEqu ETB0100)
		(isBad SES0100)
		(isDateNear EOS0100)
		(isOn AHA0100)
		(isHigh SRT0100)

    )
         
    (:goal 
        ( and

			(not(isDateNear ETB0100)) ; ETB0100
			(not(isBadEqu ETB0100)) ; ETB0100

			(not(isBad SES0100) ); SES0100 quality1 

			(not(isBadEqu ECB0100)) ;ECB0100

			(not(isBad SST0100) ); SST0100 quality1 

			(not(isOutputDone SPS0100)); SPS0100

			(not(isDateNear EOS0100)) ; EOS0100
			(not(isBadEqu EOS0100)) ; EOS0100

			(or
				(and (isHigh SHS0100) (not(isOn AHA0100)) )
				(and (not(isHigh SHS0100)) (isOn AHA0100) ) 
			) ;or SHS0100 AHA0100

			(or
				(and (isHigh SRT0100) (not(isOn ARA0100)) )
				(and (not(isHigh SRT0100)) (isOn ARA0100) ) 
			) ;or SRT0100 ARA0100

			(not(isBad SIR0100) ); SIR0100 quality1 


                  
        )
    ) 

)