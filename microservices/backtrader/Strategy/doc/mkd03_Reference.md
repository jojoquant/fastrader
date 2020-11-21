- [Reference](#reference)
  - [class backtrader.Strategy(*args, **kwargs)](#class-backtraderstrategyargs-kwargs)
  - [MA_CrossOver](#ma_crossover)
  - [SignalStrategy](#signalstrategy)

---------------------------------------------------------------------
# Reference
## class backtrader.Strategy(*args, **kwargs)
Base class to be subclassed for user defined strategies.

next()
This method will be called for all remaining data points when the minimum period for all datas/indicators have been meet.

nextstart()
This method will be called once, exactly when the minimum period for all datas/indicators have been meet. The default behavior is to call next

prenext()
This method will be called before the minimum period of all datas/indicators have been meet for the strategy to start executing

start()
Called right before the backtesting is about to be started.

stop()
Called right before the backtesting is about to be stopped

notify_order(order)
Receives an order whenever there has been a change in one

notify_trade(trade)
Receives a trade whenever there has been a change in one

notify_cashvalue(cash, value)
Receives the current fund value, value status of the strategy’s broker

notify_fund(cash, value, fundvalue, shares)
Receives the current cash, value, fundvalue and fund shares

notify_store(msg, *args, **kwargs)
Receives a notification from a store provider

buy(data=None, size=None, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None, transmit=True, **kwargs)
Create a buy (long) order and send it to the broker

data (default: None)

For which data the order has to be created. If None then the first data in the system, self.datas[0] or self.data0 (aka self.data) will be used

size (default: None)

Size to use (positive) of units of data to use for the order.

If None the sizer instance retrieved via getsizer will be used to determine the size.

price (default: None)

Price to use (live brokers may place restrictions on the actual format if it does not comply to minimum tick size requirements)

None is valid for Market and Close orders (the market determines the price)

For Limit, Stop and StopLimit orders this value determines the trigger point (in the case of Limit the trigger is obviously at which price the order should be matched)

plimit (default: None)

Only applicable to StopLimit orders. This is the price at which to set the implicit Limit order, once the Stop has been triggered (for which price has been used)

trailamount (default: None)

If the order type is StopTrail or StopTrailLimit, this is an absolute amount which determines the distance to the price (below for a Sell order and above for a buy order) to keep the trailing stop

trailpercent (default: None)

If the order type is StopTrail or StopTrailLimit, this is a percentage amount which determines the distance to the price (below for a Sell order and above for a buy order) to keep the trailing stop (if trailamount is also specified it will be used)

exectype (default: None)

Possible values:

Order.Market or None. A market order will be executed with the next available price. In backtesting it will be the opening price of the next bar

Order.Limit. An order which can only be executed at the given price or better

Order.Stop. An order which is triggered at price and executed like an Order.Market order

Order.StopLimit. An order which is triggered at price and executed as an implicit Limit order with price given by pricelimit

Order.Close. An order which can only be executed with the closing price of the session (usually during a closing auction)

Order.StopTrail. An order which is triggered at price minus trailamount (or trailpercent) and which is updated if the price moves away from the stop

Order.StopTrailLimit. An order which is triggered at price minus trailamount (or trailpercent) and which is updated if the price moves away from the stop

valid (default: None)

Possible values:

None: this generates an order that will not expire (aka Good till cancel) and remain in the market until matched or canceled. In reality brokers tend to impose a temporal limit, but this is usually so far away in time to consider it as not expiring

datetime.datetime or datetime.date instance: the date will be used to generate an order valid until the given datetime (aka good till date)

Order.DAY or 0 or timedelta(): a day valid until the End of the Session (aka day order) will be generated

numeric value: This is assumed to be a value corresponding to a datetime in matplotlib coding (the one used by backtrader) and will used to generate an order valid until that time (good till date)

tradeid (default: 0)

This is an internal value applied by backtrader to keep track of overlapping trades on the same asset. This tradeid is sent back to the strategy when notifying changes to the status of the orders.

oco (default: None)

Another order instance. This order will become part of an OCO (Order Cancel Others) group. The execution of one of the orders, immediately cancels all others in the same group

parent (default: None)

Controls the relationship of a group of orders, for example a buy which is bracketed by a high-side limit sell and a low side stop sell. The high/low side orders remain inactive until the parent order has been either executed (they become active) or is canceled/expires (the children are also canceled) bracket orders have the same size

transmit (default: True)

Indicates if the order has to be transmitted, ie: not only placed in the broker but also issued. This is meant for example to control bracket orders, in which one disables the transmission for the parent and 1st set of children and activates it for the last children, which triggers the full placement of all bracket orders.

**kwargs: additional broker implementations may support extra parameters. backtrader will pass the kwargs down to the created order objects

Example: if the 4 order execution types directly supported by backtrader are not enough, in the case of for example Interactive Brokers the following could be passed as kwargs:


orderType='LIT', lmtPrice=10.0, auxPrice=9.8
This would override the settings created by backtrader and generate a LIMIT IF TOUCHED order with a touched price of 9.8 and a limit price of 10.0.

Returns

the submitted order
sell(data=None, size=None, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None, transmit=True, **kwargs)
To create a selll (short) order and send it to the broker

See the documentation for buy for an explanation of the parameters

Returns: the submitted order

close(data=None, size=None, **kwargs)
Counters a long/short position closing it

See the documentation for buy for an explanation of the parameters

Note

size: automatically calculated from the existing position if not provided (default: None) by the caller
Returns: the submitted order

cancel(order)
Cancels the order in the broker

buy_bracket(data=None, size=None, price=None, plimit=None, exectype=2, valid=None, tradeid=0, trailamount=None, trailpercent=None, oargs={}, stopprice=None, stopexec=3, stopargs={}, limitprice=None, limitexec=2, limitargs={}, **kwargs)
Create a bracket order group (low side - buy order - high side). The default behavior is as follows:

Issue a buy order with execution Limit

Issue a low side bracket sell order with execution Stop

Issue a high side bracket sell order with execution Limit.

See below for the different parameters

data (default: None)

For which data the order has to be created. If None then the first data in the system, self.datas[0] or self.data0 (aka self.data) will be used

size (default: None)

Size to use (positive) of units of data to use for the order.

If None the sizer instance retrieved via getsizer will be used to determine the size.

Note

The same size is applied to all 3 orders of the bracket

price (default: None)

Price to use (live brokers may place restrictions on the actual format if it does not comply to minimum tick size requirements)

None is valid for Market and Close orders (the market determines the price)

For Limit, Stop and StopLimit orders this value determines the trigger point (in the case of Limit the trigger is obviously at which price the order should be matched)

plimit (default: None)

Only applicable to StopLimit orders. This is the price at which to set the implicit Limit order, once the Stop has been triggered (for which price has been used)

trailamount (default: None)

If the order type is StopTrail or StopTrailLimit, this is an absolute amount which determines the distance to the price (below for a Sell order and above for a buy order) to keep the trailing stop

trailpercent (default: None)

If the order type is StopTrail or StopTrailLimit, this is a percentage amount which determines the distance to the price (below for a Sell order and above for a buy order) to keep the trailing stop (if trailamount is also specified it will be used)

exectype (default: bt.Order.Limit)

Possible values: (see the documentation for the method buy

valid (default: None)

Possible values: (see the documentation for the method buy

tradeid (default: 0)

Possible values: (see the documentation for the method buy

oargs (default: {})

Specific keyword arguments (in a dict) to pass to the main side order. Arguments from the default **kwargs will be applied on top of this.

**kwargs: additional broker implementations may support extra parameters. backtrader will pass the kwargs down to the created order objects

Possible values: (see the documentation for the method buy

Note

This kwargs will be applied to the 3 orders of a bracket. See below for specific keyword arguments for the low and high side orders

stopprice (default: None)

Specific price for the low side stop order

stopexec (default: bt.Order.Stop)

Specific execution type for the low side order

stopargs (default: {})

Specific keyword arguments (in a dict) to pass to the low side order. Arguments from the default **kwargs will be applied on top of this.

limitprice (default: None)

Specific price for the high side stop order

stopexec (default: bt.Order.Limit)

Specific execution type for the high side order

limitargs (default: {})

Specific keyword arguments (in a dict) to pass to the high side order. Arguments from the default **kwargs will be applied on top of this.

High/Low Side orders can be suppressed by using:

limitexec=None to suppress the high side

stopexec=None to suppress the low side

Returns

A list containing the 3 orders [order, stop side, limit side]

If high/low orders have been suppressed the return value will still contain 3 orders, but those suppressed will have a value of None

sell_bracket(data=None, size=None, price=None, plimit=None, exectype=2, valid=None, tradeid=0, trailamount=None, trailpercent=None, oargs={}, stopprice=None, stopexec=3, stopargs={}, limitprice=None, limitexec=2, limitargs={}, **kwargs)
Create a bracket order group (low side - buy order - high side). The default behavior is as follows:

Issue a sell order with execution Limit

Issue a high side bracket buy order with execution Stop

Issue a low side bracket buy order with execution Limit.

See bracket_buy for the meaning of the parameters

High/Low Side orders can be suppressed by using:

stopexec=None to suppress the high side

limitexec=None to suppress the low side

Returns

A list containing the 3 orders [order, stop side, limit side]

If high/low orders have been suppressed the return value will still contain 3 orders, but those suppressed will have a value of None

order_target_size(data=None, target=0, **kwargs)
Place an order to rebalance a position to have final size of target

The current position size is taken into account as the start point to achieve target

If target > pos.size -> buy target - pos.size

If target < pos.size -> sell pos.size - target

It returns either:

The generated order
or

None if no order has been issued (target == position.size)
order_target_value(data=None, target=0.0, price=None, **kwargs)
Place an order to rebalance a position to have final value of target

The current value is taken into account as the start point to achieve target

If no target then close postion on data

If target > value then buy on data

If target < value then sell on data

It returns either:

The generated order
or

None if no order has been issued
order_target_percent(data=None, target=0.0, **kwargs)
Place an order to rebalance a position to have final value of target percentage of current portfolio value

target is expressed in decimal: 0.05 -> 5%

It uses order_target_value to execute the order.

Example

target=0.05 and portfolio value is 100

The value to be reached is 0.05 * 100 = 5

5 is passed as the target value to order_target_value

The current value is taken into account as the start point to achieve target

The position.size is used to determine if a position is long / short

If target > value

buy if pos.size >= 0 (Increase a long position)
sell if pos.size < 0 (Increase a short position)
If target < value

sell if pos.size >= 0 (Decrease a long position)
buy if pos.size < 0 (Decrease a short position)
It returns either:

The generated order
or

None if no order has been issued (target == position.size)
getsizer()
Returns the sizer which is in used if automatic statke calculation is used

Also available as sizer

setsizer(sizer)
Replace the default (fixed stake) sizer

getsizing(data=None, isbuy=True)
Return the stake calculated by the sizer instance for the current situation

getposition(data=None, broker=None)
Returns the current position for a given data in a given broker.

If both are None, the main data and the default broker will be used

A property position is also available

getpositionbyname(name=None, broker=None)
Returns the current position for a given name in a given broker.

If both are None, the main data and the default broker will be used

A property positionbyname is also available

getpositionsbyname(broker=None)
Returns the current by name positions directly from the broker

If the given broker is None, the default broker will be used

A property positionsbyname is also available

getdatanames()
Returns a list of the existing data names

getdatabyname(name)
Returns a given data by name using the environment (cerebro)

add_timer(when, offset=datetime.timedelta(0), repeat=datetime.timedelta(0), weekdays=[], weekcarry=False, monthdays=[], monthcarry=True, allow=None, tzdata=None, cheat=False, *args, **kwargs)
Note

Can be called during __init__ or start

Schedules a timer to invoke either a specified callback or the notify_timer of one or more strategies.

Parameters

when (-) – can be

datetime.time instance (see below tzdata)

bt.timer.SESSION_START to reference a session start

bt.timer.SESSION_END to reference a session end

offset which must be a datetime.timedelta instance

Used to offset the value when. It has a meaningful use in combination with SESSION_START and SESSION_END, to indicated things like a timer being called 15 minutes after the session start.

repeat which must be a datetime.timedelta instance

Indicates if after a 1st call, further calls will be scheduled within the same session at the scheduled repeat delta

Once the timer goes over the end of the session it is reset to the original value for when

weekdays: a sorted iterable with integers indicating on which days (iso codes, Monday is 1, Sunday is 7) the timers can be actually invoked

If not specified, the timer will be active on all days

weekcarry (default: False). If True and the weekday was not seen (ex: trading holiday), the timer will be executed on the next day (even if in a new week)

monthdays: a sorted iterable with integers indicating on which days of the month a timer has to be executed. For example always on day 15 of the month

If not specified, the timer will be active on all days

monthcarry (default: True). If the day was not seen (weekend, trading holiday), the timer will be executed on the next available day.

allow (default: None). A callback which receives a datetime.date` instance and returns True if the date is allowed for timers or else returns False

tzdata which can be either None (default), a pytz instance or a data feed instance.

None: when is interpreted at face value (which translates to handling it as if it where UTC even if it’s not)

pytz instance: when will be interpreted as being specified in the local time specified by the timezone instance.

data feed instance: when will be interpreted as being specified in the local time specified by the tz parameter of the data feed instance.

Note

If when is either SESSION_START or SESSION_END and tzdata is None, the 1st data feed in the system (aka self.data0) will be used as the reference to find out the session times.

cheat (default False) if True the timer will be called before the broker has a chance to evaluate the orders. This opens the chance to issue orders based on opening price for example right before the session starts

*args: any extra args will be passed to notify_timer

**kwargs: any extra kwargs will be passed to notify_timer

Return Value:

The created timer
notify_timer(timer, when, *args, **kwargs)
Receives a timer notification where timer is the timer which was returned by add_timer, and when is the calling time. args and kwargs are any additional arguments passed to add_timer

The actual when time can be later, but the system may have not be able to call the timer before. This value is the timer value and no the system time.

## MA_CrossOver
## SignalStrategy