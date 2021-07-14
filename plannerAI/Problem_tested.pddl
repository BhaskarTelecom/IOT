(define (problem SMSProblem)

    (:domain SMSDomainFile)
    
    (:objects	
    
    	pressure1 - pressure
    	roomTemp1 - roomTemp 
    	humdity1  - humitdity
    	
    	IR1 - InfraRed
    	ESD1 - esdProtection
    	soldering1 - solderingTemp
    	
    	tempAct1  - tempActuator
    	humidAct1 - humidityAcutator
    	
    	log1   - logistics
    	main1 - maintainence
    	quality1 - quality
    	
    	tb1 - equipment
    	osc1 - equipment
    	conv1 - equipment
    	

    )
    
    (:init
        
        (isHigh roomTemp1)
        (isOn tempAct1)
        
        (isHigh humdity1)
        (isOn humidAct1)
        
        (isBad IR1)
        (isBad ESD1)
        (isBad soldering1)
        ;(not(isInformed quality))
        
        (isDateNear tb1)
        (isDateNear osc1)
        ;(isDateNear conv1)
        
        (isBadEqu tb1)
        (isBadEqu osc1)
        (isBadEqu conv1)
        
        (isOutputDone pressure1)
        
    )
    
    ;; goal
        ;; 1. roomTemp_High & actTemp_OFF  or roomTemp_Low & actTemp_ON
        ;; 2. Humid_HIGH & actHum_OFF or Humid_Low & actHumid_ON
        
            ; (or	(and (isHigh roomTemp1) (not(isOn tempAct1)) )  (and (not(isHigh roomTemp1)) (isOn tempAct1) )
        
        
        ;; 3. IR_BAD & Quality_Informed
        ;; 4. ESD_BAD & Quality_Informed
        ;; 5. solder_BAD & Quality_Informed
        
        ;or ( and (not(isBad IR1)) (isInformed quality1) )
        
        ;; 6. tb_dateNear & Main_informed
        ;; 7. osc_dateNear & Main_informed
        ;; 
        
        ; ( and  (isDateNear tb1) (isInformed main1))
        
        ;; 9. tb_BAD & Main_informed
        ;; 10. osc_BAD & Main_informed
        ;; 11. conv_BAD & Main_informed
        
        ; ( and  (isBadEqu tb1) (isInformed main1))
        
        ;; 12. pres_HIGH & Logistics_Informed
        
        
        
        
        
        
    (:goal ( and (and (not(isBad IR1)) (isInformedQuality quality1 IR1)) 
    
                  (and (not(isBad ESD1)) (isInformedQuality quality1 ESD1))
                  
                  (and (not(isBad soldering1)) (isInformedQuality quality1 soldering1))
                  
                  
                  (or	(and (isHigh roomTemp1) (not(isOn tempAct1)) )  
                        (and (not(isHigh roomTemp1)) (isOn tempAct1) ) 
                  )
                  
                  (or	(and (isHigh humdity1) (not(isOn humidAct1)) )  
                        (and (not(isHigh humdity1)) (isOn humidAct1) ) 
                  )
                 
                  (isInformedDate main1 tb1)
                  (isInformedDate main1 osc1)
                  
                  (isInformedBadEqu main1 tb1)
                  (isInformedBadEqu main1 osc1)
                  (isInformedBadEqu main1 conv1)
                  
                  (isInformedLogistics log1 pressure1)
                  
            )
    ) 

)