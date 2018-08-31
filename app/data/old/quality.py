from app.logosinsights.logospersonutils import get_firebase
db = get_firebase(db=True)
data1 = {
'postId': "TESTPOST2",
    "topic": "Science",
    "userId":"USERID4",
    'title': 'Cooking oil coating prevents bacteria from growing on food processing equipment',
    "post": """"Many foods produced on an industrial scale include raw ingredients mixed together in enormous stainless steel machines that can be difficult to clean. With repeated use, equipment surfaces get minute scratches and grooves, providing bacteria and biofilms the perfect place to hide. While surface scratches may appear small to the naked eye, they are like a canyon to bacteria, which are only a few micrometers in size. Surface-trapped food residue and bacteria then increase the risk of contamination from microorganisms such as Salmonella, Listeria and E. coli.

Professor Ben Hatton (MSE), Dr. Dalal Asker and Dr. Tarek Awad research cheaper, safer and more effective ways to prevent bacteria thriving inside these machines. This minimizes the risk of cross contamination, which can lead to foodborne disease. Their team have proposed a simple new solution: trapping a thin layer of cooking oil at the metal surface to fill in microscopic scrapes, cracks and fissures and create a barrier to bacterial attachment.

They found that this solution resulted in a 1,000x reduction in bacterial levels inside the industrial machines tested. Their work is recently published in the journal ACS Applied Materials & Interfaces.

“Coating a stainless steel surface with an everyday cooking oil has proven remarkably effective in repelling bacteria,” says Hatton who collaborated on the project with AGRI-NEO, an Ontario seed processing company looking for a solution to a common problem in its industry. “The oil fills in the cracks, creates a hydrophobic layer and acts as a barrier to contaminants on the surface.”

Food particles can accumulate on an untreated stainless steel surface, at left, increasing the risk of contamination in food production facilities. The oil-treated surface, at right, repels material. (Credit: Liz Do)
Food particles can accumulate on an untreated stainless steel surface, at left, increasing the risk of contamination in food production facilities. The oil-treated surface, at right, repels material. (Credit: Liz Do)
This simple and cost-effective alternative builds on the Slippery Liquid-Infused Porous Surfaces (SLIPS) principle, initially developed at Harvard to trap lubricant layers into a surface microstructure and create slippery, non-wetting and non-adhesive properties. Cooking oils such as olive, corn or canola also provide a safer option for cleaning food-processing equipment than the harsh chemicals and disinfectants that are typically used. The sheer size of the machines makes it harder for cleaning materials to do a thorough job, and leftover bacteria can build up resistance to the cleaning agents. Hatton’s method of filling the scratches with oil prevents bacteria from settling and essentially cleans the surface without leaving chemical residues on the stainless steel surface.

“Contamination in food preparation equipment can impact individual health, cause costly product recalls and can still result after chemical-based cleaning occurs,” says Hatton. “The research showed that using a surface treatment and a cooking oil barrier provides greater coverage and results in 1,000 less bacteria roaming around.”

The Hatton research group continues to test new combinations of oils, foods and biofilm types to increase the efficiency of the bacteria barriers.  They will also explore options of using this method in developing countries to minimize bacterial infection and improve mortality rates.""",
'comment1': {
"userId": 'TESTUSER1',
        'commentId': "TESTCOMMENT3",
    'text': "Oil becomes incredibly difficult to remove from surfaces when heated or left on a surface for a long time. Anyone with an exhaust hood above their stove tops have likely noticed solidified oil that's nearly impossible to remove without harsh cleaners and a lot of elbow grease. Hopefully there\'s a way to combat this side effect.",
'reply1': {
    "userId": "TESTUSER2",
    "comments": """I just buy cheap degreaser in store. I cover hood in degreaser for about 2 minutes and then I just wipe it with off. It takes no effort and degreaser has even nice smell.
        Even my mother at her house said that it is to much work to clean her hood. It took me 15 minutes to clean her hood so it looked like brand new after 3 years of neglect.""",
    "commentId": "TESTCOMMENT10"
    ,
        "replyId": "TESTREPLY7"
        }},

    'comment2': {
        "comments": """I work in this field for pharma/cosmetics. Current cleaning practices are great at removing most residual product/micro contamination from product contact surfaces. However, micro contamination still happens, prompting research like this to find better ways to prevent microbes from hanging around between batches. Production managers tend to think “We didn’t clean it hard enough, so now we have to clean harder and stronger”
What’s usually happening- contamination finds other ways into the product. One example- a company I worked with kept seeing certain organisms in their final product. Their solution was to double the cleaning cycle time and chemical concentrations. Counts ended up increasing! What was actually happening- the extra heat of the cleaning cycle caused gaskets to loosen for water to leak out. This water flowed over non- product contact mechanical areas, and dripped back down into the bottles as they were being filled! A second example when I edit....
Edit- second example- when a company I worked with first started up new equipment, they saw HUGE micro counts in their early production stream. This was after cleaning the equipment with their normal cycles. The company contracted a cleaning company for some extra cleaning of the lines with some pretty harsh sporicides, and sure enough, the next lot made was totally clean. When the routine cleaning started back up, the organisms came back. This really stuck in the heads of production management that harder, stronger cleaning was needed. The real story this time- the routine cleaning process was programmed to cover all the product contact areas incorrectly, so a section of pipe ~2meters long wasn’t getting routinely cleaned. When the company came in to do their special cleaning, they followed the product flow path exactly, which is why their cleaning worked, and the routine cleaning didn’t.
Moral of the story, it’s great to have better coatings/cleanings when needed, but these companies need to be looking at causes outside of what’s expected."""
        ,
        "commentId": "TESTCOMMENT4",
        'userId': "TESTUSER3",
        'postId': "TESTPOST2",

    },
    'comment3': {
        "comments":"""""",
        'commentId': "TESTCOMMENT5",
        'userId': "TESTUSER2",
        'postId': 'TESTPOST2'
    }


}

data2 = {
'postId': "TESTPOST3",
    "userId": "TESTUSER9",
    "topic": "Beauty & Fitness",
    'title': 'Effects of dietary macronutrient distribution on resting and post-exercicse.',
    "post": """Previous research has demonstrated that habitual dietary macronutrient distribution affects energy substrate utilization at rest and during exercise. The primary purpose of the current study was to examine the relationships between habitual baseline macronutrient intakes, expressed relative to bodyweight and percentage of total energy intake, and metabolism at rest and after exercise in women. Twenty recreationally active women (Mean ± SD; Age 24.6 ± 3.9 yrs; Height 164.4 ± 6.6 cm; Weight 62.7 ± 6.6 kg; BF% 28.2 ± 4.8%) volunteered for the current study. Prior to metabolic testing, participants completed strength testing to determine their 1RM for six resistance exercises and completed a 3-day dietary log. Participants were provided with detailed instructions for accurately logging food intake and portion sizes, and instructed to record their regular food intake on two week days and one weekend day. Logs were analyzed using The Food Processor software (ESHA Research, Salem, OR, USA). Body composition was determined using dual-energy X-ray absorptiometry (DXA). Exercise was prescribed using baseline strength data and heart rate reserve calculations. Respiratory exchange ratio (RER) and resting energy expenditure (REE) were analyzed via indirect calorimetry (Parvomedics TrueOne 2400) before exercise (PRE), and during minutes 0-10 (IP), 25-35 (30min), and 50-60 (60min) post-exercise. Bivariate correlations and independent samples t-tests were completed using SPSS software (Version 19.0; IBM, Somers, NY, USA). Participants were stratified based on fat intake as a percentage of total caloric intake (high fat > 35% of total kcals, n=11; low fat < 35% of total kcals, n=9) and relative to bodyweight (high fat > 1.3 g/kg, n=11; low fat < 1.3 g/kg, n=9). Consent to publish the results was obtained from all participants.""",
    'comment1': {
        "userId": 'TESTUSER2',
        'commentId': "TESTCOMMENT6",
        'text': "If you want to be really simple to the point of possible inaccuracy. As long as you get your essential fatty acids, you're good. That's like people recommending ~20 grams of protein to stimulate protein synthesis adequately. That is just the amount that will likely give you enough leucine. 25% of your calories may be the amount that will likely give you sufficient EFAs. You can get your EFAs with way less fat though."
                ,
        'reply1': {
        "userId": "TESTUSER3",
        "comments": """I've heard to up carbs and lower fat on refeeds but why exactly?""",
        "commentId": "TESTCOMMENT6",
        "replyId": "TESTREPLY7"
    }},

    'comment2': {
        "comments": """"The leptin replenishment is an additional reason and the reason you lower fats is because with the higher carbs, those fats go straight to (body) fat (rather than getting burned off due to low glycogen levels imposed by the hypocaloric diet).
So, you do the refeeds for the following reasons:
1) Glycogen replenishment, leading to (assuming a sufficient refeed phase lasting more than one tiny meal)
2) Hormone repair (e.g., leptin level recovery (I should note that T3 and TST recovery would take much longer than "a couple of days" (e.g., 6 months to a year for full recovery after a prolonged diet))), leading to
3a) Metabolism repair (your body knows it's starving and tries to reduce metabolism to compensate (i.e., not all of the loss in metabolism comes from weight loss, alone) ), and
3b) Psychological repair (arguably optional, from a physiological view, but cortisol effects still happen)
..., while doing this, you try to avoid fat storage (by eating less fat, while going eu- or hypercaloric by increasing the (low glycemic index? debated...) carbohydrate load)."""
        ,
        "commentId": "TESTCOMMENT7",
        'userId': "TESTUSER1",
        'postId': "TESTPOST3",

    },
    'comment3': {
        "comments":"""Looks like a solid study to me, interesting results. Quite a lot higher fat intake than the usually recommended 20% of total kcal. I wonder if this: "Participants consuming > 1.3 g/kg of fat per day trended toward lower fat mass (p=0.09) and BF% (p=0.07)." is related to them being full faster from eating more calorie dense foods, and under-reporting their calorie intake. It makes no sense for there to be such a big difference in fat mass and bf% if the total calories are the same.""",
        'commentId': "TESTCOMMENT8",
        'userId': "TESTUSER1",
        'postId': 'TESTPOST3'
    }


}

def insert(data):
    db.child("postcontent").child(data['postId']).set({"content": data['post'], 'userId': data['userId']})
    comment1 = data['comment1']
    reply1 = comment1['reply1']

    comment2 = data['comment2']

    comment3 = data['comment3']

    db.child("postcomments").child(comment1['commentId']).set(comment1)

    db.child("commentsonpostcomments").child(reply1['replyId']).set(reply1)

    db.child("postcomments").child(comment2['commentId']).set(comment2)

    db.child("postcomments").child(comment3['commentId']).set(comment3)

    #db.child("postcomments").child(comment1['commentId']).set(comment3)

if __name__ == "__main__":
    insert(data1)
    insert(data2)