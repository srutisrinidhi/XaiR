from .model_interface.gpt_image_recog import ask_gpt_3_5, ask_gpt
import numpy as np
from tqdm import tqdm

folders_gt = ["/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/humidifier", "/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/making coffee","/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/sandwich","/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/Setting Table", "/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/Soldering responses"]
folders = ['/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/video_segments/humidifier/', '/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/video_segments/coffee/', '/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/video_segments/sandwich/', '/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/video_segments/setting table/', '/home/ssrinidh/Sruti/cognitive-assistant/results/Ego-centric Videos/video_segments/soldering/']
intent = ["set up a humidifier.", "make coffee.", "make a sandwich.", "set up a dinner table.", "solder."]

instruction_count = []
for (cnt,folder) in tqdm(enumerate(folders)):
    if (cnt !=2):
        continue
    groundTruthfile = folders_gt[cnt] + "/ground_truth.txt"
    groundTruthfile = open(groundTruthfile, "r")
    groundTruth = groundTruthfile.read()

    outputFile = folder + "/instructionCount.txt"
    outputFile = open(outputFile, "w+")

    statsFile = folder + "/stats.txt"
    statsFile = open(statsFile, "w+")

    Allscores = []
    inst_count = {"correct":0, "wrong":0, "extra":0, "total":0}
    per_file_count = {"correct":0, "wrong":0, "extra":0, "total":0}
    for i in tqdm(range(10)):
        AIResponseFile = folder + "/llava_inst_%d.txt"%i
        AIResponseFile = open(AIResponseFile, "r")
        AIResponse = AIResponseFile.read()
        
        currentScores = []
        interim_count = {"correct":0, "wrong":0, "extra":0, "total":0}
        for j in range(10):

            # prompt = '''I am giving you two set of instructions to ''' + intent[cnt] + ''' The first set is the ground truth and the second one has been generated by an AI model. Can you tell me how accurate the AI model is and give me a score between 1 and 10? If there are additional details in the AI model's response that explain the steps in the ground truth, that is still considered correct.

            # Ground truth: '''+ groundTruth + '''

            # AI model: ''' + AIResponse + '''

            # Give me just the score and not an explanation. You have to give me an answer'''
            prompt = '''I am giving you two set of instructions to ''' + intent[cnt] + ''' The first set is the ground truth and the second one has been generated by an AI model. Can you tell me what percentage of the AI's instructions are correct, how many are wrong and how many are extra? Also tell me how many instructions are there in total.
            Ground truth: '''+ groundTruth + '''
            AI model: ''' + AIResponse + '''
            Give it to me in the format and no extra information:
              Correct instructions=___
              Wrong instructions=___
              Extra instructions=___
              Total instructions=___'''
            answer = ask_gpt(prompt=prompt, views=[])
            print(answer)
            lines = answer.splitlines()
            prev_digit = False
            for val in lines[3].split("Total instructions")[1]:
                if val.isdigit():
                    if not prev_digit:
                        number = val
                        prev_digit = True
                    else:
                       number = number + val 
                       break
                else:
                    if prev_digit:
                        break
            inst_count["total"] = int(number)
            interim_count["total"] = int(number)
            prev_digit = False
            for val in lines[0].split("Correct instructions")[1]:
                if val.isdigit():
                    if not prev_digit:
                        number = val
                        prev_digit = True
                    else:
                       number = number + val 
                       break
                else:
                    if prev_digit:
                        break
            inst_count["correct"] += int(number)/inst_count["total"] 
            interim_count["correct"] += int(number)/interim_count["total"]
            prev_digit = False
            for val in lines[1].split("Wrong instructions")[1]:
                if val.isdigit():
                    if not prev_digit:
                        number = val
                        prev_digit = True
                    else:
                       number = number + val 
                       break
                else:
                    if prev_digit:
                        break
            inst_count["wrong"] += int(number)/inst_count["total"] 
            interim_count["wrong"] += int(number)/interim_count["total"]
            prev_digit = False
            for val in lines[2].split("Extra instructions")[1]:
                if val.isdigit():
                    if not prev_digit:
                        number = val
                        prev_digit = True
                    else:
                       number = number + val 
                       break
                else:
                    if prev_digit:
                        break
            inst_count["extra"] += int(number)/inst_count["total"] 
            interim_count["extra"] += int(number)/interim_count["total"]
            
            outputFile.write(answer + '\n')
        for key in interim_count.keys():
            interim_count[key] /=10
            per_file_count[key] += interim_count[key]
        statsFile.write("File %d = "%i + str(interim_count))
    outputFile.write(str(inst_count))
    outputFile.close()
    for key in per_file_count.keys():
        per_file_count[key] /=10
    statsFile.write("Overall average counts) = " + str(per_file_count))
    statsFile.close()
    instruction_count.append(inst_count)
    #         print(answer)
    #         for val in answer:
    #             if val.isdigit():
    #                 currentScores.append(int(val))
    #                 break
    #     print(currentScores)
    #     Allscores.append(currentScores)

    # Allscores = np.array(Allscores)
    # Averages = np.mean(Allscores, 1)

    # TotalAverage = np.mean(Averages)

    # outputFile.write("Total Accuracy Score = " + str(TotalAverage) + '\n')

    # outputFile.write("Accuracy Score per output= ")
    # outputFile.write(str(Averages))
    # outputFile.write('\n')

    # outputFile.write("Raw Accuracy Scores = ")
    # outputFile.write( str(Allscores))
    # outputFile.write('\n')



    # outputFile.close()
    # # #break

print(instruction_count)