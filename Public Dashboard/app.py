#imports
from shiny import App, ui, render, reactive
import shinyswatch
import pandas as pd
import seaborn as sns
from pathlib import Path
import matplotlib.pylab as plt
import matplotlib as mpl
import numpy as np
import script
import matplotlib.ticker as mtick
from shiny.types import ImgData

#data frames
HMS = pd.read_csv(Path(__file__).parent / 'HMS_Public.csv', low_memory=False)
SDF = pd.read_csv(Path(__file__).parent / 'SDF.csv', low_memory=False)
SDF2 = pd.read_csv(Path(__file__).parent / 'SDF2.csv', low_memory=False)
HMS.drop(HMS[(HMS['yr_sch']==0)].index, inplace=True)
sns.set_palette("plasma")


#Dictionaries and Lists
SubUseDemo = {"race": "Race",
              "yr_sch": "Class Year",
              "survey": "Annual Trends (Select 'All Years')",
              "Sexual orientation": "LGBTQ+ status",
              "international": "International student",
              "GenderID": "Gender",
              }
Percent= {"Percent Male": "Men",
          "Percent Women": "Women",
          "Percent Black": "Black/African American",
          "Percent White": "White",
          "Percent Asian": "Asian",
          "Percent Hispanic/Latino": "Hispanic/Latino",
          "Percent Surveyed": "Overall population",
          "Percent International": "International",
          }
Count= ["Men", 
        "Women", 
        "Hispanic/Latino", 
        "Black or African American", 
        "White", 
        "Asian",
        "American Indian or Alaska Native",
        "Two or more races"]  
YearList= ["All years", 2017, 2018, 2019, 2020, 2022]
YearList1920= [2019, 2020]
CompScore= {"diener_full_score": "flourishing score",
            "deprawsc": "Depression screen score",
            "anx_score": "Anxiety screen score"}

#Ui beginning section
app_ui = ui.page_fluid(
    shinyswatch.theme.sandstone(),
    ui.h1("Improving Student Wellness"),
    ui.row(
        ui.column(8,ui.input_select('year', "Select Year", YearList), ),
        ui.column(2,ui.output_image('DLlogo',),style='width:168px;height:168px'),),

    ui.navset_tab(
#Overview Tab is missing text in the individual sections (get done by Friday)
        ui.nav("Overview",
            ui.h2("Overview and Demographics"),
            ui.h3("What is the Healthy Minds Survey?"),
            ui.markdown(script.WhatisHMS),
            ui.h3("What Our Team Did"),
            ui.markdown(script.WWD),
            ui.h3("Navigating Our Dashboard"),
            ui.markdown(script.NavDash),
            ui.h3("Who Filled out the Healthy Minds survey?"),
            ui.input_select('d1', "select demographic", Percent),
            ui.output_plot("demoplot1"),
            ui.input_select('d2', "select demographic", Count),
            ui.output_plot("demoplot2"),
            ui.markdown("Some demographics such as American Indian/Alaska Native were moved into the 'other' category for future race sorted demographics due to their small population size."),
            ui.h4("Resources"),
            ui.h4("University Counseling and Psychological Services:"),
            ui.markdown("https://new.sewanee.edu/campus-life/flourishing/wellness-commons/university-wellness-center/counseling-and-psychological-services-caps/"),
            ui.markdown("Phone: (931) 598-1325"),
            ui.markdown("Email: caps@sewanee.edu"),
            ui.markdown("24/7 Wellness Center Crisis Line: (931) 598-1700"),
            ui.markdown("Nationwide Mental Health Emergency and Suicide Prevention Hotline: 988"),
            ui.markdown("SAMHSA’s National Helpline: 1-800-662-HELP (4357) or TTY: 1-800-487-4889 or text your zip code to 435748 (HELP4U)"),
            ui.h4("Sexual assault resources:"),
            ui.markdown("Chattanooga Rape Crisis Center: 423-755-2700"),
            ui.markdown("24-Hour Sexual Assault Violence Response Team (Nashville): 1-800-879-1999"),
            ui.markdown("RAINN (Rape, Abuse & Incest National Network): 1-800-656-4673"),
            ui.markdown("Southern Tennessee Regional Hospital - Sewanee: 931-598-5691"),
            ui.h4("Substance abuse resources:"),
            ui.markdown("FindTreatment.gov"),
            ui.markdown("Drug-Free Workplace Helpline: 1-800-WORKPLACE (967-5752)"),
            ui.markdown("Email: dwp@samhsa.hhs.gov"),


            ),
        
#Social Isolation 5 questions

        ui.nav("Social Isolation",
            ui.h2("Social Isolation"),
            ui.markdown(script.SLdefs),
            ui.p("* Class Year refers to the question \"What year are you in your current degree program?\", where 1 = 1st Year, 2 = 2nd Year, etc."),
            ui.input_select("x5", "Select A Demographic", SubUseDemo),
            ui.h4("How much do you agree with the following statement?: I see myself as a part of the campus community.(2017,2019,2020,2022)"),
            ui.output_plot("campus1"),

            ui.input_select("x6", "Select A Demographic", SubUseDemo),
            ui.h4("How much do you agree with the following statement?: I fit in well at my school.(2017,2019)"),
            ui.output_plot("campus2"),

            ui.input_select("x7", "Select A Demographic", SubUseDemo),
            ui.h4("How much do you agree with the following statement?: I feel isolated from campus life.(2017,2019)"),
            ui.output_plot("campus3"),

            ui.input_select("x8", "Select A Demographic", SubUseDemo),
            ui.h4("I feel I belong at this school.(2018,2020)"),
            ui.output_plot("campus4"),
            
            ui.input_select("x9", "Select A Demographic", SubUseDemo),
            ui.h4("I have a group, community, or social circle at Sewanee where I feel I belong (feel at home, known, connected to, supported in my identity)(2018,2020)"),
            ui.output_plot("campus5"),

#Mental Health Utilization 3 questions

            ),
        ui.nav("Mental Health Utilization",
            ui.h2("Mental Health Status and Service Utilization"),

            ui.p("* Class Year refers to the question \"What year are you in your current degree program?\", where 1 = 1st Year, 2 = 2nd Year, etc."),
            ui.input_select("mh1", "Select A Demographic", SubUseDemo, selected = "survey"),
            ui.h3("If you were experiencing serious emotional distress, whom would you talk to about this? (Percentage of people who said 'No one')"),
            ui.output_plot("mhplot1"),

            ui.input_select("mh2", "Select A Demographic", SubUseDemo, selected = "yr_sch"),
            ui.h3("If I needed to seek professional help for my mental or emotional health, I would know where to access my school’s resources."),
            ui.output_plot("mhplot2"),

            ui.h3("About these screening tests"),
            ui.h4("Depression Screen"),
            ui.markdown(script.DepScrn),
            ui.h4("Anxiety Screen"),
            ui.markdown(script.AnxScrn),
            ui.h4("Positive Mental Health Screen"),
            ui.markdown(script.PosMHScrn),
            ui.input_select("mh3", "Select A Demographic", SubUseDemo),
            ui.input_select("mh3a", "Select A Mental Health Screen", CompScore),
            ui.h4("Comparing flourishing, anxiety and depression scores by demographic (2018+)"),
            ui.output_plot("mhplot3"),

            ui.h4("If you were experiencing serious emotional distress, whom would you talk to about this?"),
            ui.output_plot("keyplot2"),

            ui.h4("Have you ever received counseling or therapy for mental health concerns?"),
            ui.output_plot("keyplot3"),

            ui.h4("Are you currently receiving counseling or therapy?"),
            ui.output_plot("keyplot4"),


            ),
       
#Key insights, text insights and 2 outputs

        ui.nav("Key Insights",
            ui.h2("Key Insights"),
            ui.h4("Social Isolation/Loneliness"),
            ui.markdown(script.KeyInSI),
            ui.h4("Mental Health"),
            ui.markdown(script.KeyInMH),
            ui.h2('Visual insights'),
            ui.h4("Do you feel isolated from campus life?"),
            ui.output_plot("keyplot1"),


            ui.h4("How many total visits or sessions for counseling or therapy have you had in the past 12 months?"),
            ui.output_plot("keyplot5"),

            ui.h4("If you were experiencing serious emotional distress, whom would you talk to about this?"),
            ui.output_plot("keyplot8"),
            ),

#About Us Page
        ui.nav("About Us",
            ui.h2("About Our Team"),
            ui.row(
                ui.column(3,ui.output_image('AvaHS'),style='width:200px;height:200px'),
                ui.column(3,ui.output_image('JackHS'),style='width:200px;height:200px'),
                ui.column(3,ui.output_image('StevieHS'),style='width:200px;height:200px'),
                ui.column(3,ui.output_image('KeithHS'),style='width:200px;height:200px'),),
            ui.h4("Ava Justice"),
            ui.markdown(script.AvaAU),
            ui.h4("Jack Hagan"),
            ui.markdown(script.JackAU),
            ui.h4("Stevie Mack"),
            ui.markdown(script.StevieAU),
            ui.h4("Keith Young"),
            ui.markdown(script.KeithAU),
            ui.h2("What is Datalab?"),
            ui.markdown(script.WIDL),




            ),
   
        ),
    )
    
#Server, dataframes, and year filter
def server(input, output, session):
    HMS = pd.read_csv(Path(__file__).parent / 'HMS.csv', low_memory=False)
    SDF = pd.read_csv(Path(__file__).parent / 'SDF.csv', low_memory=False)
    SDF2 = pd.read_csv(Path(__file__).parent / 'SDF2.csv', low_memory=False)

    HMS['belong_8_'] = HMS.apply(lambda row:
                            row['belong8'] > 0, axis = 1)

    HMS['talk_']= HMS.apply(lambda row:
                         row['talk1_1']+
                         row['talk1_2']+
                         row['talk1_3']+
                         row['talk1_4']+
                         row['talk1_5']+
                         row['talk1_6']+
                         row['talk1_7']+
                         row['talk1_8']+
                         row['talk1_9'] > 0, axis = 1)


    HMS.drop(HMS[(HMS['yr_sch']==0)].index, inplace=True)
    HMS_Backup = HMS.copy()

    @reactive.Effect
    @reactive.event(input.year)
    def year_filter():
        if 'HMS' in dir():
            nonlocal HMS
            nonlocal HMS_Backup
            if input.year() == 'All years':
                HMS = HMS_Backup.copy()
            else:
                HMS = HMS_Backup[HMS_Backup['survey']==int(input.year())]

#Demographic Questions Output
    
    @output
    @render.plot
    @reactive.event(input.d1)   

    def demoplot1():
        plt.figure(figsize=(15,5))
        plt.xticks(rotation=45)
        plt.title(' Percentage of the university population taking HMS survey per year')
        ax = sns.barplot(x='Year',y=input.d1(),data=SDF2)
        ax.set_xticks(range(6))
        ax.bar_label(ax.containers[0], fmt='%.f%%')
        ax.set_ylabel('%')

    @output
    @render.plot
    @reactive.event(input.d2)   

    def demoplot2():
        plt.figure(figsize=(15,5))
        plt.xticks(rotation=45)
        plt.title('Number of Students at the University sorted by demographic')
        aa = sns.barplot(x='Year',y=input.d2(),data=SDF2)
        aa.set_xticks(range(6))
        for bar in aa.get_children():
            if isinstance(bar, mpl.patches.Rectangle) and bar.xy != (0,0):
                count = int(bar.get_height())
                x = bar.xy[0]
                aa.annotate(count, (x + 0.099, count + 0.025))

#Social Isolation Output

    @output
    @render.plot
    @reactive.event(input.year, input.x5)

    def campus1():
        HMS['belong_1_'] = HMS.apply(lambda row:
                            row['belong1'] > 0, axis = 1)
        axa = sns.barplot(data = HMS[HMS['belong_1_']], x = input.x5(), y = 'neg_belong1', errorbar = None)
        axa.set(xlabel = input.x5(), ylabel = 'Part of campus community', title = 'I see myself as a part of the campus community.')
        axa.set_yticks(range(6))
        axa.set_yticklabels(['Strongly Disagree', 'Disagree', 'Somewhat disagree', 'Somewhat agree', 'Agree', 'Strongly Agree'])
        plt.xticks( rotation = 40)


    @output
    @render.plot
    @reactive.event(input.year, input.x6)

    def campus2():
        HMS['belong_2_'] = HMS.apply(lambda row:
                            row['belong2'] > 0, axis = 1)
        axb = sns.barplot(data = HMS[HMS['belong_2_']], x = input.x6(), y = 'neg_belong_2', errorbar = None)
        axb.set(xlabel = input.x6(), ylabel = 'Fit in at school', title = 'I fit in well at my school')
        axb.set_yticks(range(6))
        axb.set_yticklabels(['Strongly Disagree', 'Disagree', 'Somewhat disagree', 'Somewhat agree', 'Agree', 'Strongly Agree'])
        plt.xticks( rotation = 40)


    @output
    @render.plot
    @reactive.event(input.year, input.x7)

    def campus3():
        HMS['belong_8_'] = HMS.apply(lambda row:
                            row['belong8'] > 0, axis = 1)
        axc = sns.barplot(data = HMS[HMS['belong_8_']], x = input.x7(), y = 'neg_belong8', errorbar = None)
        axc.set(xlabel = input.x7(), ylabel = 'Isolated from campus life', title = 'I feel isolated from campus life')
        axc.set_yticks(range(6))
        axc.set_yticklabels(['Strongly Disagree', 'Disagree', 'Somewhat disagree', 'Somewhat agree', 'Agree', 'Strongly Agree'])
        plt.xticks( rotation = 40)

    @output
    @render.plot
    @reactive.event(input.year, input.x8)

    def campus4():
        HMS['exp_belong_1_'] = HMS.apply(lambda row:
                            row['exp_belong'] > 0, axis = 1)
        axd=sns.barplot(data = HMS[HMS['exp_belong_1_']], x = input.x8(), y = 'neg_exp_belong', errorbar = None)
        axd.set(xlabel = input.x7(), ylabel = 'Belong at school', title = 'I feel I belong at this school')
        axd.set_yticks(range(6))
        axd.set_yticklabels(['Strongly Disagree', 'Disagree', 'Somewhat disagree', 'Somewhat agree', 'Agree', 'Strongly Agree'])


    @output
    @render.plot
    @reactive.event(input.year, input.x9)

    def campus5():
        HMS['group_belong_1_'] = HMS.apply(lambda row:
                            row['group_belong'] > 0, axis = 1)
        axe=sns.barplot(data = HMS[HMS['group_belong_1_']], x = input.x9(), y = 'neg_group_belong', errorbar = None)
        axe.set(xlabel = input.x7(), ylabel = 'Group on campus', title = 'I have a group, community, or social circle at Sewanee where I feel I belong')
        axe.set_yticks(range(6))
        axe.set_yticklabels(['Strongly Disagree', 'Disagree', 'Somewhat disagree', 'Somewhat agree', 'Agree', 'Strongly Agree'])

#Mental Health Outputs

    @output
    @render.plot
    @reactive.event(input.year, input.mh1)

    def mhplot1():
        sns.barplot(data = HMS[HMS['talk_']], y = 'talk1_9' , x = input.mh1() , errorbar = None)
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))

    @output
    @render.plot
    @reactive.event(input.year, input.mh2)


    def mhplot2():
        
        plt.figure(figsize=(15,5))
        plt.xticks(rotation=45)
        plt.title('HMS survey by knowledge of campus services')
        ax= sns.countplot(x=input.mh2(),hue='KnowledgeCampR',data=HMS)
        for bar in ax.get_children():
            if isinstance(bar, mpl.patches.Rectangle) and bar.xy != (0,0):
                count = int(bar.get_height())
                x = bar.xy[0]
                ax.annotate(count, (x + 0.049, count + 3))
        
    @output
    @render.plot
    @reactive.event(input.year, input.mh3, input.mh3a)

    def mhplot3():

        xx=sns.barplot(data = HMS, x = input.mh3(), y = input.mh3a(), errorbar = None)
        for bar in xx.get_children():
            if isinstance(bar, mpl.patches.Rectangle) and bar.xy != (0,0):
                count = int(bar.get_height())
                x = bar.xy[0]
                xx.annotate(count, (x + 0.049, count + 0.5))
    
#Key Insights Outputs

    @output
    @render.plot


    def keyplot1():


        aj = sns.barplot(data = HMS[HMS['belong_8_']], x = 'GenderID', y = 'neg_belong8', errorbar = None)
        aj.set(xlabel = 'Gender', ylabel = 'Isolated from campus life', title = 'Student who feel isolated from campus life')
        aj.set_yticks(range(7))
        aj.set_yticklabels(['','Strongly Disagree', 'Disagree', 'Somewhat disagree', 'Somewhat agree', 'Agree', 'Strongly Agree'])
        plt.xticks( rotation = 40)

    
    @output
    @render.plot


    def keyplot2():

        ac = sns.barplot(data = HMS[HMS['talk_']], x = 'talk1_9' , y = 'diener_full_score' , errorbar = None)
        plt.xticks(rotation = 45)
        ac.set(ylabel = 'Positive Mental Health Score', xlabel = 'Emotional support', title = 'Emotional Distress Support')
        ac.set_xticklabels(['Emotional support', 'Lacking emotional support'])
    

    @output
    @render.plot

    def keyplot3():

        HMS['new_ther_ever'] = HMS.apply(lambda row:
                                row['ther_ever'] > 0, axis = 1)

        ab = sns.barplot(data = HMS[HMS['new_ther_ever']], x = 'ther_ever', y = 'diener_full_score', errorbar = None)
        ab.set_xticklabels(['No, never', 'Yes, prior to starting college', 'Yes, since start of college', 'Yes, both of the above'])
        plt.xticks(rotation = 40)
        ab.set(ylabel = 'Mental Health Score', xlabel = 'Use of therapy', title = 'Mental Health Score/Use of Therapy')
    

    @output
    @render.plot

    def keyplot4():

        ad = sns.barplot(data = HMS, x = 'ther_cur', y = 'diener_full_score', errorbar = None)
        ad.set(ylabel = 'Mental Health Score', xlabel = 'Current Use of Therapy', title = 'Mental Health Score/Current Use of Therapy')
        ad.set_xticklabels(['No', 'Yes'])


    @output
    @render.plot

    def keyplot5():

        ae = sns.barplot(data = HMS, y = 'ther_vis', x = 'GenderID', errorbar = None)
        ae.set(xlabel = 'Gender', ylabel = 'Number of Visits', title = 'Gender/Number of Visits')


    @output
    @render.plot

    def keyplot8():

        ap = sns.barplot(data = HMS[HMS['talk_']], x = 'talk1_1' , y = 'GenderID' , errorbar = None)
        plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
        ap.set(ylabel = 'Gender', xlabel = 'Professional Clinician', title = 'Students who feel they can talk to a clinician')





#Images
    @output
    @render.image
    def WClogo():
        return ImgData(src=str(Path(__file__).parent / 'WellnessCenterLogo.jpg'),
            height='168px', width='168px')

    @output
    @render.image
    def DLlogo():
        return ImgData(src=str(Path(__file__).parent / 'DataLabLogo.png'),
            height='168px', width='168px')

    @output
    @render.image
    def AvaHS():
        return ImgData(src=str(Path(__file__).parent / 'Ava.jpg'),
            height='200px', width='200px')

    @output
    @render.image
    def JackHS():
        return ImgData(src=str(Path(__file__).parent / 'Jack.jpg'),
            height='200px', width='200px')
    
    @output
    @render.image
    def StevieHS():
        return ImgData(src=str(Path(__file__).parent / 'Stevie.jpg'),
            height='200px', width='200px')
    
    @output
    @render.image
    def KeithHS():
        return ImgData(src=str(Path(__file__).parent / 'Keith.jpg'),
            height='200px', width='200px')


app = App(app_ui, server)
