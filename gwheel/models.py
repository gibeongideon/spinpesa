from django.db import models
from django.contrib.auth.models import User
# from django.db import transaction
from django.db.models import Sum #,Count, Sum, F ,OuterRef
from datetime import timedelta #,timezone ,datetime,
from random import randint
from django.utils import timezone
from core.models import TimeStamp,BetSettingVar,Market,MarketType,Selection 
from account.models import Account,TransactionLog
# from core.functions.models_settings import set_up

from core.models import BetSettingVar

def set_up():
    try:
        return BetSettingVar.objects.get(id =1)# Set up variables
    except:
        BetSettingVar.objects.update_or_create(id =1)
        return BetSettingVar.objects.get(id =1)


class WheelSpin(Market): 
    market = models.ForeignKey(MarketType,on_delete=models.CASCADE,related_name='wp_markets',blank =True,null= True)   
    # per_relief = models.FloatField(blank =True,null= True)

    def __str__(self):
        return 'WheelSpin({0})'.format(self.id)

    def market_selection_id_list(self):
        return self.market.this_market_selection_id_list()


    def total_bet_amount_per_marktinstance(self):
        try:
            total_amount = Stake.objects.filter(market_id = self.id ).aggregate(bet_amount =Sum('amount'))
            return  total_amount.get('bet_amount')

        except Exception as e:
            return e

    @property
    def black_bet_amount(self):
        try:
            total_amount = Stake.objects.filter(market_id = self.id ).filter(marketselection_id = 1).aggregate(bet_amount =Sum('amount'))
            if total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
 
            return  0
            
        except Exception as e:
            return e

    @property
    def white_bet_amount(self):

        try:
            total_amount = Stake.objects.filter(market_id = self.id ).filter(marketselection_id = 2).aggregate(bet_amount =Sum('amount'))
            if  total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return 0
            
        except Exception as e:
            return e
    def market_stake_amount(self,select_id):

        try:
            total_amount = Stake.objects.filter(market_id = self.id ).filter(marketselection_id = select_id).aggregate(bet_amount =Sum('amount'))
            if  total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return 0
        
        except Exception as e:
            return e

    @property
    def selection_bet_amount(self):
        mrkt_bet_amount= []
        for selecn in self.market_selection_id_list():
            mrkt_bet_amount.append(self.market_stake_amount(selecn))

        return mrkt_bet_amount



    @property
    def offset(self):
        try:
            return abs(self.white_bet_amount - self.black_bet_amount)

        except Exception as e:
            return e
    @property
    def gain_after_relief(self):
        per_to_return = set_up().per_retun
        return ((100 - per_to_return)/100)*float(self.offset)


    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on staking  '''

        if self.active and not self.place_stake_is_active:
            self.active = False
        try:
            self.market = MarketType.objects.get( id= int(set_up().wheelspin_id) )
        except:
            self.market = MarketType.objects.get( id= 1)

        if not self.pk:
        
            try:
                self.closed_at = self.open_at + timedelta(minutes = set_up().closed_at)
                self.results_at = self.open_at + timedelta(minutes =set_up().results_at)

            except Exception as e:
                print('MRKTINSTS:',e)
                pass
            
        super().save(*args, **kwargs) 



# def per_returnn(self,all_gain,user,all_lose_stake,per_to_return):  ##CRITICAL FUCTION/MUST WORK PROPERLY
#     try:
#         return_amount = (per_to_return/100)*all_gain
#         per_user_return = (user/all_lose_stake)*return_amount
#         return per_user_return

#     except Exception as e:
#         print('RESUUUU111',e)
#         return 50




class Stake (TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_wp_stakes',blank =True,null=True)
    market = models.ForeignKey(WheelSpin, on_delete=models.CASCADE,related_name='wheelspins',blank =True,null=True)
    marketselection = models.ForeignKey(Selection, on_delete=models.CASCADE,related_name='marketselections',blank =True,null=True)
    current_bal = models.FloatField(max_length=10,default=0 )#R
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    # outcome = models.CharField(max_length=200,blank =True,null=True)

    stake_placed = models.BooleanField(blank =True,null=True)
    has_record = models.BooleanField(blank =True,null=True)

    def __str__(self):
        return 'Stake:{0} for:{1}'.format(self.amount,self.user)

    @property
    def account_bal(self):
        try:
            ac_bal = float(Account.objects.get(user_id =self.user_id).balance)
            return ac_bal
        except Exception as e:
            return e   

    @property
    def place_bet_is_active(self):
        return self.market.place_stake_is_active

    def update_account_on_win_lose(self):
        selection = self.marketselection_id
        try:
            results = Result.objects.get(market_id = self.market_id).resu  #self.marketinstant.determine_result_algo
        except:
            results = ''
        resu = ''
        try:
            if not results:
                resu = 'PENDING'               
            elif selection == results:
                resu= 'YOU WIN'
            else:
                resu = 'YOU LOSE'
            return resu
            
        except Exception as e:
            print('GERR',e)
    
    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on staking  '''
        if not self.stake_placed:
            market_id = max((obj.id for obj in WheelSpin.objects.all())) #  check if generator can help
           
            market_is_active= WheelSpin.objects.get(id =market_id ).place_stake_is_active

            if market_is_active:

                self.market = WheelSpin.objects.get(id =market_id )
                try:
                    ctotal_balanc = Account.objects.get(user_id = self.user_id).balance
                    if self.amount <= ctotal_balanc:
                        if not self.stake_placed:
                            new_bal = ctotal_balanc - self.amount
                            self.current_bal = new_bal
                            Account.objects.filter(user_id=self.user_id).update(balance= new_bal)
                            self.stake_placed = True
                    
                    else: 
                        raise Exception ('No cash')
                        # return 'Not enough balance to stake'

                except Exception as e:
                    print('STAKE:',e)
                    return

            else:
                print('INACTIVE MARKET!')
                return # no saving record if market is inactive

            try:

                if not self.has_record:
                    TransactionLog.objects.create(user_id =self.user_id,amount= self.amount ,trans_type = 'Stake')
                    self.has_record = True
            except:
                pass


            super().save(*args, **kwargs)


class CumulativeGain(TimeStamp):

    gain = models.FloatField(default=0, blank =True,null= True)

    @property
    def gainovertime(self): 

        try:
            total_amount = Result.objects.filter(cumgain_id = self.id ).aggregate(cum_amount =Sum('gain'))
            if  total_amount.get('cum_amount'):
                return total_amount.get('cum_amount')
            return total_amount
            
        except Exception as e:
            print(e)
            return e

class Result(TimeStamp):

    market = models.OneToOneField(WheelSpin,on_delete=models.CASCADE,related_name='rmarkets',blank =True,null= True)
    cumgain = models.ForeignKey(CumulativeGain,on_delete=models.CASCADE,related_name='gains',blank =True,null= True)

    resu = models.IntegerField(blank =True,null= True)
    return_per =models.FloatField(blank =True,null= True)
    gain = models.DecimalField(('gain'), max_digits=100, decimal_places=5,blank =True,null= True)

    closed = models.BooleanField(blank =True,null= True)
    active = models.BooleanField(blank =True,null= True)

    @property
    def determine_result_algo(self):  # fix this
        try:
            B = self.market.black_bet_amount
            W = self.market.white_bet_amount
            
            if self.market.instance_is_active == False:
                if B == W:
                    return randint(1,2) # fix me to get random 1 or 2
                if B > W :
                    return 2
                return 1

        except Exception as e:
            return  e

    def resu_velocity_map(self):
        from random import randint
        red1= randint(7000,7500)
        # red2= randint(7700,8200)
        # red3= randint(8300,8600)
        # red4= randint(8700,8900)
        

        white1= randint(7000,7500)
        # white2= randint(7700,8200)
        # white3= randint(8300,8600)
        # white4= randint(8700,8900)

        if self.determine_result_algo ==2:
            return  red1
        else:
            return white1

    def per_returnn(self,all_gain,user,all_lose_stake,per_to_return):  ##CRITICAL FUCTION/MUST WORK PROPERLY
        try:
            return_amount = (per_to_return/100)*all_gain
            per_user_return = (user/all_lose_stake)*return_amount
            return per_user_return

        except Exception as e:
            print('RESUUUU111',e)
            return 50

    def update_reference_account(self,user_id,ref_credit,trans_type):
        print(user_id,ref_credit,trans_type)

        try:
            user_details = UserDetail.objects.filter(user_id = user_id)
            print('USER DETAILS',user_details)

            for  user_detail in user_details:
                refer_code = user_detail.refer_code
                print('referCODE{0}'.format(refer_code))

                # if refer_code:
                referer_details = UserDetail.objects.filter(own_refer_code = refer_code)
                print('referer details:',referer_details)
                try:

                    for referer_detail in referer_details:
                        r_user_id = referer_detail.user_id
                        print(r_user_id,'userIDDS')
                        RefAccountCredit.objects.create(user_id = r_user_id, amount= ref_credit)
                except Exception as e:
                    print ('REF',e)


                    # ref_account_bal = float(Account.obje  cts.get(user_id = r_user_id).refer_balance)
                # new
            # else:
                # pass
                    # RefAccountCredit.objects.create(user_id = 1, amount= ref_credit)# ADMIN id 1
        except Exception as e:

            print('REFER E',e)
            

    def update_acc_n_bal_record(self,user_id,new_bal,amount,trans_type):
        try:          
            Account.objects.filter(user =user_id).update(balance= new_bal)
            TransactionLog.objects.create(user_id =user_id,amount= amount ,trans_type = trans_type)

        except Exception as e:
            print('RESUUUUp',e)

            

    def account_update(self):
            try:
                all_stakes_in_this_market = Stake.objects.filter(marketinstant = self.market).all()
                for _stake in all_stakes_in_this_market: 
                    user_id = _stake.user_id


                    for  user in Stake.objects.filter(id = _stake.id ): # 
                        ctotal_balanc = float(Account.objects.get(user_id = user_id).balance)
                        amount = float(user.amount)

                        if user.marketselection_id == self.resu:
                            new_bal = ctotal_balanc + amount*2 
                            amount = round(amount*2)

                            per_for_referer =5  # Settings 
                            ref_credit = (per_for_referer/100)*amount
                            rem_credit = amount -ref_credit

                            trans_type = 'WIN' 
                            self.update_acc_n_bal_record(user_id,new_bal,rem_credit,trans_type)

                            trans_type = 'R-WIN'
                            self.update_reference_account(user_id,ref_credit,trans_type)

                        elif user.marketselection_id != self.resu:
                            all_gain = float(self.market.offset)
                            userstake =  float(user.amount)
                            if self.resu == 2:
                                all_lose_stake = float(self.market.black_bet_amount)
                            elif self.resu ==1:
                                all_lose_stake = float(self.market.white_bet_amount)

                            per_to_return = float(set_up().per_retun) # 

                            relief_amount = self.per_returnn(all_gain,userstake,all_lose_stake,per_to_return)
                            new_bal = ctotal_balanc + relief_amount
                            amount= round(relief_amount,1)
                            trans_type = 'ROL'
                            self.update_acc_n_bal_record(user_id,new_bal,amount,trans_type)  
                                                                                          
                    self.closed= True

            except Exception as e:
                print('RESULTACCOUNT:',e)
                return
                
    def update_db_records(self):
        try:
            set_per_return = set_up().per_retun
            self.return_per =set_per_return
            self.gain = self.market.gain_after_relief
            WheelSpin.objects.filter(id =self.market_id).update(closed =True) # self.market.update(closed=True) or self.market.closed=True DOESN'T WORK
            
        except Exception as e:
            print('RESULT RECORDS:',e)
            pass


    def save(self, *args, **kwargs):  
        ''' Overrride internal model save method to update balance on staking  '''

        self.resu = self.determine_result_algo

        if  self.resu and not self.closed:

            self.update_db_records()
            self.account_update()
            self.market.closed = True
            super().save(*args, **kwargs) #save only if 

        else:
            return
# super().save(*args, **kwargs)