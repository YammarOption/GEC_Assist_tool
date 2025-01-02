local moneyAddr = 0xd573
local tiDAddr = 0xd1a1
local nameAddr = 0xd1a3
local frame_pause = 60*4
local framecounter = 0
local sock = nil

function ST_stop()
	if not sock then return end
	console:log("sock Test: Shutting down")
	sock:close()
	sock = nil
end

function opensock()
	console:log("--------------------------------")
    ST_stop()
	console:log("sock Test: Connecting to 127.0.0.1:9999")
	if sock then return end
	sock = socket.tcp()
	if sock:connect("127.0.0.1", 9999) then
		console:log("sock Test: Connected")
	else
		console:log("sock Test: Failed to connect")
		ST_stop()
	end
end

function updateTracker()
    local money = emu:read8(moneyAddr)<<16|emu:read8(moneyAddr+1)<<8|emu:read8(moneyAddr+2)
    local tID = emu:read8(tiDAddr)<<8|emu:read8(tiDAddr+1)
    local name = emu:read8(nameAddr)<<32|emu:read8(nameAddr+1)<<24|
				emu:read8(nameAddr+2)<<16|emu:read8(nameAddr+3)<<8|
				emu:read8(nameAddr+4)
	console:log(string.format("%i",money))
	console:log(string.format("%i",tID))
	console:log(string.format("%x",name))
    if not sock then return end
	sock:send("MONEY:"..string.format("%x",money).."@ID:"..string.format("%x",tID).."@NAME:"..string.format("%x",name))
end


function updateBuffer()
    framecounter=framecounter+1
    if framecounter >= frame_pause then
    	updateTracker()
        framecounter=0
    end
end

callbacks:add("frame", updateBuffer)
callbacks:add("start",opensock)
callbacks:add("error",ST_stop)
callbacks:add("stop",ST_stop)
callbacks:add("shutdown",ST_stop)
