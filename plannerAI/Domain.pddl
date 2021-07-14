(define (domain SMSDomainFile)

    (:requirements
        [:adl]
    )

    (:types
        
        actuator equipment sensor person - object
        actSensor qualitySensor pressure - sensor
        humitdity roomTemp - actSensor
		InfraRed esdProtection solderingTemp - qualitySensor
		tempActuator humidityAcutator - actuator
		logistics maintainence quality - person
		convyor testbentch oscilloscope - equipment

    )


    (:predicates
    
        ;; for sensor
        (isHigh ?x - actSensor)
        (isBad  ?x - qualitySensor)
        (isOutputDone ?x - pressure)
        
        
        ;;for actuator
        (isOn ?x - actuator)
        
        ;;for equipment
        (isDateNear ?x - equipment)
        (isBadEqu ?x - equipment)
        
        ;;for person
        (isInformedDate ?x - maintainence ?e - equipment)
        (isInformedBadEqu ?x - maintainence ?e - equipment)
        (isInformedQuality ?x - quality ?s - qualitySensor )
        (isInformedLogistics ?x - logistics ?s - pressure)
        
    
    )


;;action section 
    ;;for actuators
    (:action turnON 
        :parameters (?s - actSensor ?a - actuator)
        :precondition (and (not(isHigh ?s)) (not(isOn ?a)))
        :effect (isOn ?a)
    )
    
    (:action turnOFF 
        :parameters (?s - actSensor ?a - actuator)
        :precondition (and (isHigh ?s) (isOn ?a))
        :effect (not(isOn ?a))
    )
    
    ;;for person
    (:action aleartMaintainanceDate
        :parameters (?e - equipment ?p - maintainence)
        :precondition (and (isDateNear ?e)  (not (isInformedDate ?p ?e)) )  
        :effect  (and (isInformedDate ?p ?e) (not(isDateNear ?e)))
    )
    
    (:action aleartMaintainanceBadEqu
        :parameters (?e - equipment ?p - maintainence)
        :precondition (and (isBadEqu ?e) (not (isInformedBadEqu ?p ?e)) )
        :effect  (and (isInformedBadEqu ?p ?e)  (not(isBadEqu ?e)) )       
                    
    )
    
    (:action aleartLogistics
    
        :parameters (?s - pressure ?p -  logistics)
        :precondition (and (isOutputDone ?s) (not(isInformedLogistics ?p ?s)) )
        :effect (and (not(isOutputDone ?s)) (isInformedLogistics ?p ?s) )
    )
    
    (:action aleartQuality
        :parameters (?s - qualitySensor ?p - quality)
        :precondition (and (isBad ?s) (not(isInformedQuality ?p ?s)) )
        :effect (and (not(isBad ?s)) (isInformedQuality ?p ?s) )
    )
    
    
)   