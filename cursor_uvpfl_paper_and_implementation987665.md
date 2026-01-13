# UVPFL paper and implementation
_Exported on 1/13/2026 at 12:00:03 GMT+5:30 from Cursor (2.3.34)_

---

**User**

the files u can see is the implementation of the paper document.pdf UVPFL , i will feed u that paper section by section , u need to learn eachj anad everything so that later u can understand the implementaion that i have done using cursor somewhere else and optimize and modify it , lets start with the paper first 

---

**Cursor**


Reviewing the paper and the implementation document to understand UVPFL.



Reading the paper in sections, starting with the beginning to understand its structure:



The PDF is in binary format. Searching for readable text sections and checking the implementation document for context:



Ready to learn the paper section by section. From what I've seen:

**UVPFL (User Profile-Based Viewport Prediction Using Federated Learning)** is a system for:
- Predicting user viewports in 360-degree video streaming
- Using Federated Learning to profile users based on head movements
- Handling new users by matching them with similar users
- Achieving high prediction accuracy (86% in first 7 seconds, 96% overall)

**Key concepts I'm tracking:**
1. User profiling by head movements per video category
2. Federated Learning architecture for privacy-preserving training
3. Similarity matching for cold-start users
4. Viewport prediction algorithms
5. Real-time streaming requirements

Please share the paper sections. I'll:
- Understand each section thoroughly
- Ask clarifying questions if needed
- Take notes on methodology, algorithms, and implementation details
- Not implement anything until you ask

Please share the first section.

---

**User**

User Profile-Based Viewport Prediction
Using Federated Learning in
Real-Time 360-Degree Video Streaming
Syed Mohammad Haseeb ul Hassan
School of Electronic Engineering
Dublin City University
Dublin, Ireland
syed.haseebulhassan2@mail.dcu.ie
Attracta Brennan
School of Computer Science
University of Galway
Galway, Ireland
attracta.brennan@nuigalway.ie
Gabriel-Miro Muntean, Jennifer McManis
School of Electronic Engineering
Dublin City University
Dublin, Ireland
{gabriel.muntean,jennifer.mcmanis}@dcu.ie
Abstract—Streaming 360-degree videos has become increas-
ingly popular due to the growth in demand for immersive media
in recent years. Companies such as Youtube, Facebook, and
Netflix already use 360-degree video streaming. In order to reduce
the amount of data transmitted only the part of the video at which
the user looks is streamed at high resolution and enabling this re-
quires accurate viewport prediction. However, recent approaches
to streaming 360-degree video do not characterize user profiles
or have low viewport prediction accuracy when either historical
data is unavailable for the user or when the user starts watching a
new video. This paper proposes a novel approach to User Profile-
Based Viewport Prediction Using Federated Learning (UVPFL)
in 360-degree Real-Time Video Streaming. UVPFL profiles users
based on their head movements for different categories of videos.
For high viewport prediction accuracy of a new user or a user
with no historical data, UVPFL bases its viewport prediction on
the viewport of similar users. Testing UVPFL in 360-degree real-
time video streaming has resulted in an accuracy of up to 86%
for the first seven seconds of video play. UVPFL also achieved an
average accuracy of up to 96% for the complete length of video
play. UVPFL has outperformed three state-of-the-art available
viewport prediction solutions by 1.12% to 64.9% for a 1 second
prediction horizon.
Index Terms—Virtual Reality, Viewport Prediction, Multime-
dia Streaming, Federated Learning, 360-degree Video Streaming
I. INTRODUCTION
The popularity of 360-degree videos has continued to
increase, as signaled by social media trends such as the
transformation of Facebook to Meta and the creation of the
Metaverse. A Head Mounted Display (HMD) or a high-
specification mobile device is primarily used to watch these
videos [1] and use of devices continues to trend upwards.
For instance, the number of Virtual Reality (VR)-based apps
This publication has emanated from research conducted with the financial
support of the Science Foundation Ireland under Grant number 18/CRT/6224
(SFI Centre for Research Training in Digitally-Enhanced Reality D-REAL).
For the purpose of Open Access, the author has applied a CC BY public
copyright license to any Author Accepted Manuscript version arising from
this submission.
downloaded on Oculus Quest has increased by 153% from
December 2020 to December 2021 [2]. According to Cisco [3],
the minimum bandwidth required for High Definition (HD)
VR streaming and Ultra High Definition (UHD) VR streaming
is 150 Mbps and 500 Mbps, respectively. Conventional video
streaming solutions used by social media platforms such as
Youtube and Facebook deliver the entire frame to the user
simultaneously, with a minimum bandwidth requirement of
20 Mbps [4].
The high bandwidth requirements for 360-degree video
streaming have motivated interest in techniques to reduce
the amount of sent information, particularly by employing
viewport-based adaptive streaming approaches. The idea be-
hind viewport-based adaptive streaming is that for a 360-
degree video, the user watches a portion of the video (i.e.,
the viewport) displayed on their HMD. While the 360-degree
video offers a panoramic 360-degree horizontal view and a
180-degree vertical view, a viewport is typically less than 20%
of the 360-degree video and allows the user to view about 90-
degree to 120-degree horizontally and 90-degree vertically [5].
Muntean et al. [6] and Ciubotaru et al. [7] proposed a region
of interest-based adaptive multimedia streaming scheme for
2D videos and achieved up to 28% gain in peak signal-to-
noise ratio as compared to competitors. Similar solutions that
stream the viewport area at high resolution whilst streaming
other parts at low resolution may significantly decrease the
bandwidth requirement and improve the Quality of Experience
(QoE) for the user [8]. In order to successfully maintain high
QoE levels for the user, the viewport prediction algorithm must
be able to quickly and accurately predict the user’s viewport.
Viewport prediction during live video streaming includes an-
alyzing the user’s eyes and/or head movements in real-time
using computer vision techniques and Machine Learning (ML)
algorithms to predict what parts of the video users are most
likely to look at next. Feng et al. [9] predicted the viewport
in live video streaming using a simple Convolutional Neural
Network (CNN) approach and achieved an accuracy of 70-
80% depending on the complexity of the video. Chen et
al. [10] used a white box explainable approach for viewport979-8-3503-2152-4/23/$31.00 ©2023 IEEE
2023 IEEE International Symposium on Broadband Multimedia Systems and Broadcasting (BMSB) | 979-8-3503-2152-4/23/$31.00 ©2023 IEEE | DOI: 10.1109/BMSB58369.2023.10211169
Authorized licensed use limited to: Indian Institute Of Technology (Banaras Hindu University) Varanasi. Downloaded on August 12,2025 at 12:49:29 UTC from IEEE Xplore. Restrictions apply.
Fig. 1. UVPFL Viewport Prediction
prediction during live streaming and achieved an accuracy of
94% for a 1 second horizon.
A number of works have attempted to improve on the
accuracy and bandwidth reduction in the context of viewport
prediction. Feng et al. [11] predicted the viewport for lifelong
video streaming using the CNN model visual geometry group
and achieved an accuracy between 50% and 90% depending on
the video type. In non-live video streaming, it is very important
to anticipate which parts of a pre-recorded video a user will
most likely watch based on watching habits and history. This
is done to enhance the video quality and decrease the lag when
playing back the video. Park et al. [5] introduced CNN + Long
Term Short Term Memory (LSTM) and 3DCNN for viewport
prediction they also used the saliency heat map of the video
as an input. They achieved an average accuracy of 92.21% for
a 1 second horizon. The saliency of a pixel/part of a picture
defines how likely the pixel can get the attraction of the viewer.
Yaqoob et al. [12] proposed a combined Field-of-View (FoV)
tile-based adaptive streaming solution; they measured accuracy
for different tiling patterns (i.e., 4×3, 6×4, and 8×6) and for
different segments lengths (i.e., 1 second, 2 second, and 3
second) They achieved an accuracy of 58% to 78%. He et al.
[13] worked on FoV prediction for smartphone streaming and
achieved an average throughput of 0.15Mbps to 2.1Mbps for
4k videos. Wu et al. [14] used spherical CNN for viewport
prediction for stored streaming and achieved an accuracy of
40% for 10 seconds. Szab ́o et al. [15] used mulsemedia
(olfactory and haptic sensors) using CNN to improve the QoE
of the end user in 360-degree videos

---

**Cursor**


## **Abstract Summary**

**Problem:**
- Need accurate viewport prediction for 360-degree video streaming
- Current approaches don't profile users or have low accuracy for new users/new videos

**Solution (UVPFL):**
- Profiles users based on head movements per video category
- Uses Federated Learning
- For new users, leverages similar users' viewport patterns

**Results:**
- 86% accuracy for first 7 seconds
- 96% average accuracy for full video length
- Outperforms 3 state-of-the-art methods by 1.12%–64.9% (1-second horizon)

---

## **Introduction - Key Points**

### **Context & Motivation:**
1. Growing popularity: Meta/Metaverse, VR apps up 153% (Dec 2020–Dec 2021)
2. Bandwidth requirements:
   - HD VR: 150 Mbps
   - UHD VR: 500 Mbps
   - Conventional: 20 Mbps

### **Viewport-Based Adaptive Streaming:**
- Viewport = <20% of 360° video
- Dimensions: 90–120° horizontal, 90° vertical
- Strategy: High resolution for viewport, low resolution elsewhere
- Goal: Reduce bandwidth while maintaining QoE

### **Related Work (State-of-the-Art):**
1. Feng et al. [9]: CNN, 70–80% accuracy
2. Chen et al. [10]: White box explainable, 94% (1-second horizon)
3. Feng et al. [11]: VGG CNN, 50–90% (varies by video type)
4. Park et al. [5]: CNN+LSTM + 3DCNN + saliency heat maps, 92.21% average (1-second horizon)
5. Yaqoob et al. [12]: FoV tile-based, 58–78% (different tiling patterns)
6. He et al. [13]: FoV prediction for smartphones
7. Wu et al. [14]: Spherical CNN, 40% (10-second horizon)
8. Szabó et al. [15]: Multisemedia (olfactory/haptic) + CNN

### **Key Insights:**
- Saliency heat maps are used as input features
- Tile-based approaches are common
- Temporal models (LSTM) help with prediction
- Accuracy varies with prediction horizon and video complexity

Ready for the next section.

---

**User**

A. Related Works
Most current viewport prediction approaches do not address
live 360-degree video streaming for users with no historical
data [5] [16] [10]. The approach of Feng et al. [9] using
the simple CNN model AlexNet resulted in low viewport
prediction accuracy during the first 20 seconds of the video
play due to a lack of user data. It is also reported that
Facebook downloads 5 seconds of playout time [4]. However,
downloading data for playout also has limitations [17]; 1) the
user needs good network conditions to download data and, 2)
the user needs to wait until the data is downloaded; this results
in a low QoE level.
Understandably, achieving accurate early (i.e., the first few
seconds of video play) predictions of a user’s head move-
ment is challenging. However, Stefano et al. [18] achieved
an accuracy of up to 70%, 50%, and 13% for the time
horizons of 2 second, 5 second, and 10 second, respectively
by tracking the user head movement trajectories using their
trajectory-based viewport prediction approach. Flare [16] used
Linear Regression, Ridge Regression, and Supporting Vector
Machine for viewport prediction and adaptation, resulting in
an accuracy of up to 90.5%, 58.2%, and 46.7% for the 0.2
second, 1 second and 2 second horizon respectively. Mosaic
[5] used LSTM+CNN and 3DCNN for viewport prediction
and adaptation and achieved an accuracy of up to 92.21%
and 88.44% for 1 second and 2 second horizons, respectively.
Sparkle [10] used a white box explainable approach for
viewport prediction during live streaming and achieved an
accuracy of 94% and 92.21% for 1 second and 2 second
horizons, respectively.
Despite such high accuracies recorded by these studies, the
methods used cannot accurately predict viewport for the first
few seconds of a video play when no historical user data is
available. This limitation can be potentially mitigated through
the use of user profiling. In this context, user profiling refers
to the consideration of user characteristics such as interests,
age, gender, or region and how these characteristics build user
behaviour for a particular type of content [19] [20]. Currently,
available solutions lack user profiling for viewport prediction
in 360-degree video delivery.
Edge computing and distributive approaches can be used for
viewport prediction as live or stored video streaming solutions.
Edge computing solutions can serve to reduce decision time by
reducing the dependency on a centralized server and bringing
the decision-making process closer to the Edge node. This
approach is only applicable when many users are watching the
Authorized licensed use limited to: Indian Institute Of Technology (Banaras Hindu University) Varanasi. Downloaded on August 12,2025 at 12:49:29 UTC from IEEE Xplore. Restrictions apply.
same content. However, in Edge computing, one node works
as a primary node and other nodes work as secondary nodes.
Secondary nodes always depend upon primary nodes for data
processing and data storage, potentially leading to bottleneck
and processing delays. Unlike Edge computing, our approach
involves the processing and storing of data individually at
each node. Hence, we have proposed Federated Learning (FL)
solution which is a decentralized approach for the storage and
processing of the data individually at each node. Liyang et al.
[21] used caching on the Edge server for the FoV prediction.
Here a live video is streamed to multiple users watching the
same video on a local network. These users are categorized
or flocked into groups based on their latency tolerance and
how much their FoV overlapped. This approach reduces the
traffic on the core network by 80% but increases the load
on Edge nodes. Uddin et al. [22] used caching at the Edge
server to decrease latency and bandwidth loss in 360-degree
videos. These approaches help to reduce the core network’s
data transmission by performing tasks at the edge nodes.
What is Federated Learning and why it is required? FL is a
ML-based approach, where the data is stored on the client side
for training. The benefit of FL is that each user can be trained
separately and can be profiled independently. FL is widely
used in data protection, privacy, edge computing, and wireless
networks [23]. Chao et al. [24] used FL for privacy preserva-
tion in 360-degree video streaming and identified users based
on historical user data with an accuracy of up to 25.23%. Chen
et al. [25] used FL for user profiling in the aviation industry to
identify high-value passengers and achieved the Area Under
Curve value of 0.85 and Kolmogorov–Smirnov value of 0.55,
showing improvements of 9% and 31%, respectively, on
currently available solutions. Wang et al. [26] used FL for
user characteristics identification in order to learn the electric-
ity consumers’ electricity consumption pattern; the approach
achieved an accuracy of 68.5% for character identification
which was a 1.69% improvement on conventional approaches.
Zhou et al. [27] used FL for user profiling for wearable sensors
and focused on network adaptation, data consumption, and
network traffic. This approach has decreased the amount of
upload data by 29.77% and improved model accuracy by 20%.
In our approach, we used FL for profiling users separately on
the basis of their head movement in 360-degree videos.

---

**Cursor**


## **Related Works - Key Points**

### **Problem: Cold-start (no historical data)**
- Most approaches don't handle live 360° streaming for users without history
- Feng et al. [9] (AlexNet): low accuracy in first 20 seconds
- Facebook downloads 5 seconds of playout, but this has limitations:
  1. Requires good network conditions
  2. User must wait for download → low QoE

### **Early prediction challenge**
- Hard to predict in the first few seconds
- Reported accuracies:
  - Stefano et al. [18]: 70% (2s), 50% (5s), 13% (10s)
  - Flare [16]: 90.5% (0.2s), 58.2% (1s), 46.7% (2s)
  - Mosaic [5]: 92.21% (1s), 88.44% (2s)
  - Sparkle [10]: 94% (1s), 92.21% (2s)

### **Gap: user profiling**
- Current methods fail in the first few seconds without historical data
- User profiling: consider characteristics (interests, age, gender, region) and how they shape behavior per content type
- Current solutions lack user profiling for viewport prediction

### **Edge computing vs. Federated Learning**
- Edge computing:
  - Reduces decision time
  - Only when many users watch the same content
  - Primary/secondary nodes → potential bottlenecks
- UVPFL uses FL:
  - Decentralized
  - Processing and storage at each node
  - No dependency on primary nodes

### **Federated Learning (FL)**
- Definition: ML with data stored on the client side
- Benefits:
  - Each user trained separately
  - Profiled independently
  - Privacy preservation
- FL applications:
  - Chao et al. [24]: Privacy in 360° video streaming, 25.23% user identification accuracy
  - Chen et al. [25]: User profiling in aviation (AUC=0.85, KS=0.55), 9% and 31% improvements
  - Wang et al. [26]: Electricity consumption patterns, 68.5% accuracy (+1.69%)
  - Zhou et al. [27]: Wearable sensors, 29.77% less upload data, 20% accuracy improvement
- UVPFL use: Profile users separately based on head movement in 360° videos

### **Key insight**
- FL enables per-user profiling without centralizing data
- Addresses the cold-start problem by learning user-specific patterns
- Privacy-preserving and decentralized

Ready for the next section.

---

**User**

B. Our Contribution
In this paper, we use FL to predict the user’s viewport by
profiling their head movement behaviour for different types
of videos. We also propose a novel algorithm UVPFL that
bases the prediction on both the observed user head movement
and the historical viewport data. After viewport prediction, we
compare our viewport to a similar user viewport or a historical
viewport. We merge and update the predicted viewport if the
overlapping area is higher than γ. Using this approach, we
have achieved an average accuracy of up to 96% for the overall
video. During the first 7 seconds of video play, we achieved
an average accuracy of up to 86%.

---

**Cursor**


## **Our Contribution - Key Points**

### **Core approach:**
1. Federated Learning for viewport prediction
   - Profiles users based on head movement behavior
   - Profiles per video type/category

2. Novel UVPFL algorithm
   - Uses two inputs:
     - Observed user head movement (current/real-time)
     - Historical viewport data (past patterns)

3. Viewport comparison and merging
   - Compare predicted viewport with:
     - Similar user viewport, or
     - Historical viewport
   - If overlap > γ (threshold), merge and update the predicted viewport

### **Results:**
- 96% average accuracy for overall video
- 86% average accuracy for first 7 seconds (addresses cold-start)

### **Algorithm flow (inferred):**
```
1. Profile user using FL (based on head movements per video category)
2. Predict viewport using:
   - Current observed head movement
   - Historical viewport data
3. Compare predicted viewport with:
   - Similar users' viewports, OR
   - User's own historical viewports
4. If overlap > γ threshold:
   - Merge and update the predicted viewport
5. Use updated viewport for streaming
```

### **Why this addresses the problem:**
- Cold-start: Uses similar users' viewports when no history exists
- User profiling: FL profiles per video category
- Accuracy: 86% in first 7 seconds vs. lower baselines
- Privacy: FL keeps data on client side

Ready for the next section.

```plaintext
1. Profile user using FL (based on head movements per video category)
2. Predict viewport using:
   - Current observed head movement
   - Historical viewport data
3. Compare predicted viewport with:
   - Similar users' viewports, OR
   - User's own historical viewports
4. If overlap > γ threshold:
   - Merge and update the predicted viewport
5. Use updated viewport for streaming
```

---

**User**

II. PROPOSED APPROACH
A. Methodology
The motivation behind UVPFL is that similar users tend
to have similar viewing behaviour while watching 360-degree
videos. UVPFL uses FL to observe each user’s head movement
behaviour separately for different types of 360-degree videos.
The data relating to the user’s head movement behaviour is
stored on the client side. Our ML algorithm is performed
separately on each client. To test UVPFL, we used a publicly
available dataset [28] containing the head movement of 50
users and 10 videos. We modified the dataset by separating it
for each user and video category. This modification helped us
test UVPFL approach and get high accuracy for each video
and video category separately.
We have two categories of users: trained users and users
under testing. A trained user is a user who has already watched
a video using UVPFL. A test user is a person who is currently
watching the video. Data from users similar to the test users
may be used as historical data to improve the test user’s
viewport prediction. As shown in Fig. 1, Yaw (Y), Pitch (PI),
and Roll (R) angles are used to calculate the user’s current and
predicted viewport. We used a pre-trained ML model to predict
the viewport for test users; θ is the expected change of angles
(Y, PI, and R). Our key contribution involves the comparison
between the current user’s predicted viewport (VP ) and that
of a similar user (VS ) to initially extract prediction errors but
ultimately to achieve higher accuracy during the whole video.
This is shown in Fig. 1. If the overlapping area of VP and
VS is greater than γ, then UVPFL merges VP and VS . For
example, if a user is watching a video and the overlapping
area of VP and VS is higher than γ, then UVPFL merges the
two viewports.
B. UVPFL Algorithm
Our UVPFL Algorithm 1 is divided into three phases. In
Phase 1, Video processing all of the processes are performed
on the server side. With the 360-degree video and saliency
heat map provided as input, we divide the video into segments
and frames. Each frame is further divided into an lxk grid of
tiles.
In Phase 2: Viewport Prediction, all of the processes
are performed on the client side. Here the Tiles Tlk of the
current frame and saliency data of the current and similar
user are provided as input. We get the Y, PI, and R data
of the user and calculate the head movement speed of the
current user. This information is then sent as input to our
pre-trained ML model. Next, we predict the viewport VP
using the pre-trained ML algorithm. After a viewport is
predicted, our algorithm compares VP with a similar user
viewport VS . If the overlapping is greater than γ, then we
merge both viewports and update our predicted viewport.
Using the equation provided by Zou et al. [29], as shown in
Eq.(1), we calculate the visibility probability of tiles in VP
and neighbouring VP .
Authorized licensed use limited to: Indian Institute Of Technology (Banaras Hindu University) Varanasi. Downloaded on August 12,2025 at 12:49:29 UTC from IEEE Xplore. Restrictions apply.
Fig. 2. Probability Of Tiles
As shown in Fig. 2, we create different groups of tiles based
on their probabilities of being in the viewport. Group one tiles
represent VP ; Group two tiles have a probability higher than
98%; Group three tiles have a probability between 95% and
98%; Group four tiles have a probability between 90% and
95%. We next merge tiles having a probability higher than 98%
with viewport tiles. After this, we select Tlk related to VP and
identify tiles T N neighbouring to Viewport. After calculating
how much time the user spent on the previous T j−1
lk , we update
the saliency heat map of the user.
Plk ≜ P θ
lk · P φ
lk = R min{θupper
lk −θ,90◦ }
max{θlower
lk −θ,−90◦ } pθ(∆θ)d∆θ · R [φright
lk −φ]l0
[φlef t
lk −φ]l0
pφ(dφ)d∆φ (1)
In Phase 3: Tile adaptation is performed. We used a simple
hierarchical tile adaptation approach for improved QoE. The
tiles in the coordinate set VP are assigned the highest quality,
the tiles in the coordinate set neighboring viewport VN are
assigned medium quality, and the tiles in the coordinate set
VZ are assigned a low quality.

---

**Cursor**


## **II. PROPOSED APPROACH - Methodology & Algorithm**

### **A. Methodology - Core Concepts**

**Core motivation:**
- Similar users have similar viewing behavior in 360° videos

**Federated Learning approach:**
- Observe each user's head movement separately per video category
- Data stored on client side
- ML algorithm runs separately on each client
- No centralized data collection

**Dataset:**
- 50 users, 10 videos (public dataset [28])
- Modified: separated by user and video category
- Enables testing per user and category

**User categories:**
1. Trained users: Already watched a video using UVPFL
2. Test users: Currently watching the video
- Data from similar users can serve as historical data for test users

**Viewport calculation:**
- Uses Yaw (Y), Pitch (PI), Roll (R) angles
- Pre-trained ML model predicts viewport
- θ = expected change of angles (Y, PI, R)

**Key innovation:**
- Compare predicted viewport (VP) with similar user viewport (VS)
- If overlap > γ (threshold), merge VP and VS
- Improves accuracy, especially for new users

---

### **B. UVPFL Algorithm - Three Phases**

#### **Phase 1: Video Processing (Server-side)**
- Input: 360° video + saliency heat map
- Process:
  - Divide video into segments and frames
  - Divide each frame into l×k grid of tiles

#### **Phase 2: Viewport Prediction (Client-side)**
**Input:**
- Tiles Tlk of current frame
- Saliency data (current user + similar user)

**Process:**
1. Get Y, PI, R data of user
2. Calculate head movement speed
3. Send to pre-trained ML model
4. Predict viewport VP using ML algorithm
5. Compare VP with similar user viewport VS
6. If overlap > γ: merge VP and VS, update predicted viewport
7. Calculate visibility probability of tiles using Equation (1)

**Equation (1) - Tile Probability Calculation:**
```
Plk = P_lk^θ · P_lk^φ

Where:
- P_lk^θ = ∫[max{θ_lk^lower - θ_t, -90°} to min{θ_lk^upper - θ_t, 90°}] pθ(Δθ) dΔθ
- P_lk^φ = ∫[[φ_lk^left - φ]_0 to [φ_lk^right - φ]_0] pφ(Δφ) dΔφ
```

**Tile probability groups (Fig. 2):**
- Group 1: VP (predicted viewport tiles)
- Group 2: Probability > 98%
- Group 3: Probability 95%–98%
- Group 4: Probability 90%–95%

**Additional steps:**
- Merge tiles with probability > 98% with viewport tiles
- Select Tlk related to VP
- Identify neighboring tiles TN to viewport
- Calculate time spent on previous T_j-1_lk
- Update saliency heat map of user

#### **Phase 3: Tile Adaptation**
- Hierarchical tile adaptation for improved QoE
- Quality assignment:
  - VP (viewport): Highest quality
  - VN (neighboring viewport): Medium quality
  - VZ (rest): Low quality

---

### **Key Algorithm Flow:**
```
1. Server: Process video → segments → frames → tiles (l×k grid)
2. Client: 
   a. Get head movement (Y, PI, R) + speed
   b. Predict VP using ML model
   c. Compare VP with VS (similar user)
   d. If overlap > γ: merge and update
   e. Calculate tile probabilities (Eq. 1)
   f. Group tiles by probability thresholds
   g. Update saliency heat map
3. Tile Adaptation:
   - VP: Highest quality
   - VN: Medium quality  
   - VZ: Low quality
```

### **Important details:**
- γ threshold: Controls when to merge viewports
- Similar user matching: Critical for cold-start
- Saliency heat map: Updated based on user viewing time
- Probability-based tiling: Enables adaptive streaming

Ready for the next section.

```plaintext
Plk = P_lk^θ · P_lk^φ

Where:
- P_lk^θ = ∫[max{θ_lk^lower - θ_t, -90°} to min{θ_lk^upper - θ_t, 90°}] pθ(Δθ) dΔθ
- P_lk^φ = ∫[[φ_lk^left - φ]_0 to [φ_lk^right - φ]_0] pφ(Δφ) dΔφ
```

```plaintext
1. Server: Process video → segments → frames → tiles (l×k grid)
2. Client: 
   a. Get head movement (Y, PI, R) + speed
   b. Predict VP using ML model
   c. Compare VP with VS (similar user)
   d. If overlap > γ: merge and update
   e. Calculate tile probabilities (Eq. 1)
   f. Group tiles by probability thresholds
   g. Update saliency heat map
3. Tile Adaptation:
   - VP: Highest quality
   - VN: Medium quality  
   - VZ: Low quality
```

---

**User**

III. EXPERIMENTS
A. Training Setup
For training the model, we used Resnet50 Gated Recurrent
Unit (GRU), where first we chose pre-trained Resnet50, then
added time distributed layers, and then we added GRU as
shown in Fig. 3. The final output of Fig. 3 depicts the
predicted viewport, which has been used in Algorithm 1.
We used different models and parameters such as AlexNet,
MobileNet, and Resnet50 for 100 epochs. We observed that we
get the best results on parameters such as the Adam optimizer,
mean squared error loss, and 50 epochs. After 50 epochs,
there is much less change in accuracy. The accuracy achieved
by Alexnet, MobileNet, and Resnet50 is 73%, 56%, and 96%,
respectively. The input shape of the model was (30,120,240,3),
where 30, 120, 240, and 3 are frames, height, width, and
channels, respectively. We used different frames, i.e., 30, 60,
and 90, for further investigation purposes.
B. Dataset
As already mentioned, we used a publicly available dataset
[28] containing the head movement data of 50 users and
Fig. 3. Architecture Diagram for UVPFL
10 videos, with the videos categorized as (1) Computer-
Generated (CG) fast-paced, (2) Natural-Image (NI), and fast-
paced. and (3) NI, slow-paced. The length of each video was
approximately 60 seconds. In user profiling, we noted the user
head movement behaviour for each video category separately.
C. Results
We measured the accuracy for different values of the
overlapping area γ such as 70%, 80%, and 90% for a 1
second horizon. We achieved the best accuracy in the least
computational time of 648 ms at 80%. Overlapping areas less
than 80% brought little change in accuracy but required more
computational time, i.e., time for viewport prediction. Fig. 4
shows the comparison of the different γ values for the 1
second horizon. Based on these results, we performed all our
experiments with an overlapping area of γ = 80%.
We calculated the average accuracy of the video for each
user with respect to time for video category and we achieved
an average accuracy of 86% within the first 7 seconds of the video for the 1 second horizon and γ 80% (Fig. 5). We tested
UVPFL three times to validate and took the average accuracy.
We compared the proposed UVPFL approach with three
other state-of-the-art (SOTA) available approaches (1) Mosaic
[5], (2) Flare [16], and (3) Sparkle [10]. As shown in Fig. 6,
UVPFL outperformed all available approaches for a 1 second
and 2 second horizon. For a 1 second horizon, UVPFL has
shown 4.1% better results than Mosaic, 64.9% better results
Authorized licensed use limited to: Indian Institute Of Technology (Banaras Hindu University) Varanasi. Downloaded on August 12,2025 at 12:49:29 UTC from IEEE Xplore. Restrictions apply.
than Flare, and 1.12% better results than Sparkle. For a 2
second horizon, UVPFL also showed 5.32% better results
than Mosaic, 99% better results than Flare, and 0.96% better
results than Sparkle. We tested UVPFL three times for the
validation process. As shown in Table I, we achieved an
average accuracy of 96%, 93.15%, and 89% across all our
videos for the 1 second, 2 second, and 4 second horizon,
respectively. Additionally, we calculated the precision and
recall values for UVPFL. Precision is the ratio of the number
of tiles correctly predicted to be viewed to the number of tiles
to be viewed both correctly and incorrectly [5]. The higher
the value of precision, the less the prediction error. Recall
computes the difference between the predicted and the actual
number of tiles viewed. A high value of recall means that
fewer tiles are predicted incorrectly. We observed that while
the precision and recall values were very high for the 1 second
horizon, they decreased when we increased the horizon time
to 2 seconds and 4 seconds.
TABLE I
AVERAGE PREDICTION ACCURACY FOR DIFFERENT HORIZONS IN
SECONDS WITH γ VALUE 80%
Frames Accuracy Precision Recall
1 second 96 92.41 90.15
2 second 93.15 89.21 85.23
4 second 89 75.60 73.75
Furthermore, we calculated the accuracy for each video
and category separately, as shown in Fig. 7. We repeated
the test three times for validation for each video and related
category. We achieved an average accuracy of 96.6%, 95.25%,
and 96.33% for the NI fast-paced, NI slow-paced, and CG
fast-paced categories, respectively. UVPFL performs best in
fast-paced videos and provides us with the highest accuracy
compared to slow-paced videos. We observed that UVPFL per-
formed well where user head movements were more frequent.
We achieved the best results in the video Roller Coaster from
category NI fast-paced and Pacman from CG fast-paced with
an average accuracy of up to 98%. We achieved the lowest
average accuracy in the SFR Sports from category NI slow-
paced with an average accuracy of 94%. Notwithstanding, this
accuracy is higher than the accuracy of SOTA approaches.|

Algorithm 1: UVPFL algorithm
Goal: Viewport prediction
Input: 360 degree video;
Input: Saliency feature data;
PHASE 1:
Server Side Process
Divide video into N segments of time S;
foreach Segment i do
foreach Frame j do
Get saliency heat map of each F ramej ;
Get T j
lk from F ramej ▷ Client Side Process
Tlk ∈ T ← Tlk
l={1,2,3,......L}, k={1,2,3,......K}
Phase 2: Viewport Prediction
Client Side Process
Input Saliency heat map data of F ramej of
U ser;
Input: Tlk in F ramej
Calculate Y, R, PI for User;
Calculate head movement speed of U ser;
Predict viewport VP ;
if VP ∩ VS ≥ γ % then
Merge VP and VS ;
Else
VP remain same ;
end
Update VP ;
Calculate PTlk in VP F ramej [29]
Select Tlk related to VP ;
Identify T N to VP ;
Calculate how much time user spent T j−1
lk
Update user saliency heat map F ramej−1;
Phase 3:Tile Adaptation
Input: Coordinates of VP , VN , VZ (i.e., the
coordinate sets of the viewport, neighboring to
the viewport, and other areas, respectively);
Input: Tlk in F ramej
Assign low quality to all VZ ;
Assign medium quality to all VN ;
Assign high quality to all VP ;
end
end

---

**Cursor**


## **III. EXPERIMENTS - Complete Details**

### **A. Training Setup**

**Model Architecture (Fig. 3):**
- ResNet50 (pre-trained) → Time Distributed layers → GRU
- Output: Predicted viewport (used in Algorithm 1)

**Model Comparison:**
- Tested: AlexNet, MobileNet, ResNet50
- Epochs: 100 (best results at 50 epochs)
- Best configuration:
  - Optimizer: Adam
  - Loss: Mean Squared Error
  - Epochs: 50 (little change after 50)
- Accuracy results:
  - AlexNet: 73%
  - MobileNet: 56%
  - ResNet50: 96% (selected)

**Input Shape:**
- `(30, 120, 240, 3)`
  - 30 = frames (sequence length)
  - 120 = height
  - 240 = width
  - 3 = channels (RGB)
- Also tested: 30, 60, 90 frames

---

### **B. Dataset**

- Public dataset [28]
- 50 users, 10 videos
- Video categories:
  1. Computer-Generated (CG) fast-paced
  2. Natural-Image (NI) fast-paced
  3. Natural-Image (NI) slow-paced
- Video length: ~60 seconds each
- User profiling: Head movement behavior tracked per video category separately

---

### **C. Results**

#### **1. Overlapping Threshold γ Selection:**
- Tested: γ = 70%, 80%, 90% (1-second horizon)
- Best: γ = 80%
  - Best accuracy
  - Least computational time: 648 ms
  - γ < 80%: Little accuracy gain, more computational time
- All experiments use γ = 80%

#### **2. Accuracy for First 7 Seconds:**
- Average accuracy: 86% (first 7 seconds, 1-second horizon, γ = 80%)
- Validated: Tested 3 times, averaged

#### **3. Comparison with SOTA (Fig. 6):**

**1-second horizon:**
- UVPFL: 96%
- Sparkle: 94% (UVPFL +1.12%)
- Mosaic: 92% (UVPFL +4.1%)
- Flare: 58% (UVPFL +64.9%)

**2-second horizon:**
- UVPFL: 92%
- Sparkle: 92% (UVPFL +0.96%)
- Mosaic: 88% (UVPFL +5.32%)
- Flare: 46% (UVPFL +99%)

#### **4. Average Accuracy by Horizon (Table I):**

| Horizon | Accuracy | Precision | Recall |
|---------|----------|-----------|--------|
| 1 second | 96%      | 92.41%    | 90.15% |
| 2 second | 93.15%   | 89.21%    | 85.23% |
| 4 second | 89%      | 75.60%    | 73.75% |

**Metrics:**
- Precision: Ratio of correctly predicted tiles to total predicted tiles (higher = less prediction error)
- Recall: Difference between predicted and actual tiles viewed (higher = fewer incorrect predictions)
- Both decrease as horizon increases

#### **5. Accuracy by Video Category (Fig. 7):**
- NI fast-paced: 96.6%
- CG fast-paced: 96.33%
- NI slow-paced: 95.25%
- Best performance: Fast-paced videos (more frequent head movements)
- Best video: Roller Coaster (NI fast-paced) and Pacman (CG fast-paced) → 98%
- Lowest: SFR Sports (NI slow-paced) → 94% (still higher than SOTA)

---

### **Algorithm 1: Complete UVPFL Algorithm**

**Goal:** Viewport prediction

**Input:**
- 360-degree video
- Saliency feature data

**PHASE 1: Server Side Process**
```
1. Divide video into N segments of time S
2. For each Segment i:
   For each Frame j:
     - Get saliency heat map of Frame_j
     - Get T_lk^j from Frame_j (tiles)
     - T_lk ∈ T ← T_lk
     - l = {1,2,3,...,L}, k = {1,2,3,...,K}
```

**PHASE 2: Viewport Prediction (Client Side Process)**
```
Input:
- Saliency heat map data of Frame_j of User
- T_lk in Frame_j

1. Calculate Y, R, PI for User (Yaw, Roll, Pitch)
2. Calculate head movement speed of User
3. Predict viewport V_P
4. if V_P ∩ V_S ≥ γ % then
     Merge V_P and V_S
   Else
     V_P remain same
   end
5. Update V_P
6. Calculate P_Tlk in V_P Frame_j [using Eq. 1]
7. Select T_lk related to V_P
8. Identify T_N to V_P (neighboring tiles)
9. Calculate how much time user spent T_lk^(j-1)
10. Update user saliency heat map Frame_(j-1)
```

**PHASE 3: Tile Adaptation**
```
Input:
- Coordinates of V_P, V_N, V_Z
- T_lk in Frame_j

1. Assign low quality to all V_Z (other areas)
2. Assign medium quality to all V_N (neighboring viewport)
3. Assign high quality to all V_P (viewport)
end
```

---

### **Key Implementation Details:**

1. Model: ResNet50 + Time Distributed + GRU
2. Input: (30, 120, 240, 3) - 30 frames sequence
3. γ threshold: 80% (optimal)
4. Prediction horizons: 1s, 2s, 4s
5. User profiling: Per video category
6. Similar user matching: Critical for cold-start
7. Tile quality: Hierarchical (high/medium/low)

Ready for the next section.

```plaintext
1. Divide video into N segments of time S
2. For each Segment i:
   For each Frame j:
     - Get saliency heat map of Frame_j
     - Get T_lk^j from Frame_j (tiles)
     - T_lk ∈ T ← T_lk
     - l = {1,2,3,...,L}, k = {1,2,3,...,K}
```

```plaintext
Input:
- Saliency heat map data of Frame_j of User
- T_lk in Frame_j

1. Calculate Y, R, PI for User (Yaw, Roll, Pitch)
2. Calculate head movement speed of User
3. Predict viewport V_P
4. if V_P ∩ V_S ≥ γ % then
     Merge V_P and V_S
   Else
     V_P remain same
   end
5. Update V_P
6. Calculate P_Tlk in V_P Frame_j [using Eq. 1]
7. Select T_lk related to V_P
8. Identify T_N to V_P (neighboring tiles)
9. Calculate how much time user spent T_lk^(j-1)
10. Update user saliency heat map Frame_(j-1)
```

```plaintext
Input:
- Coordinates of V_P, V_N, V_Z
- T_lk in Frame_j

1. Assign low quality to all V_Z (other areas)
2. Assign medium quality to all V_N (neighboring viewport)
3. Assign high quality to all V_P (viewport)
end
```

---

**User**

IV. CONCLUSION
In this work, we proposed a novel approach to User
Profile-Based Viewport Prediction Using Federated Learning
(UVPFL) in 360-degree real-time video streaming. UVPFL
addresses viewport prediction accuracy issues when historical
data is unavailable for the user or when the user starts
watching a new video. UVPFL profiles the user and performs
viewport prediction with high accuracy for new users or users
with no historical data. First, UVPFL profiles the user by
head movement data for different video categories. Next, it
compares the predicted viewport with a similar user viewport.
If the overlapping area is higher than 80%, it merges the
viewports.
Fig. 7. Accuracy for each video
To check the effectiveness of UVPFL, we performed several
experiments using a publicly available dataset [28] containing
the head movement data of 50 users and 10 videos. UVPFL
achieved an average accuracy of 96% for viewport predic-
tion. UVPFL outperformed the existing approaches Mosaic,
Flare, and Sparkle by 4.1%, 6.07%, and 1.12%, respectively.
However, we believe that there are still opportunities for
improvement in UVPFL. Due to data limitations, we only
profile users’ head movements in different video categories.
In the future, we plan to profile users based on eye movement
data, regional impact on user response, and user behaviour to
interact with different objects to improve performance

---

**Cursor**


## **IV. CONCLUSION - Summary & Future Work**

### **Summary of UVPFL Approach:**

**Problem addressed:**
- Viewport prediction accuracy when historical data is unavailable
- Cold-start problem (new users or new videos)

**Solution:**
1. Profile users by head movement data per video category
2. Compare predicted viewport with similar user viewport
3. Merge viewports if overlap > 80% (γ = 80%)

**Key innovation:**
- Uses similar users' viewports for new users
- Federated Learning for privacy-preserving user profiling

---

### **Experimental Validation:**

**Dataset:**
- 50 users, 10 videos (public dataset [28])

**Results:**
- Average accuracy: 96% for viewport prediction
- Outperformed SOTA:
  - Mosaic: +4.1%
  - Flare: +6.07%
  - Sparkle: +1.12%

**Note:** The conclusion mentions 6.07% improvement over Flare (may be an average across horizons), while earlier results showed 64.9% for 1-second horizon specifically.

---

### **Future Work & Limitations:**

**Current limitation:**
- Only profiles users' head movements per video category
- Data limitations constrained the scope

**Future improvements planned:**
1. Eye movement data profiling
2. Regional impact on user response
3. User behavior for interaction with different objects

**Potential enhancements:**
- Multi-modal profiling (head + eye movements)
- Geographic/cultural factors
- Object-level interaction patterns
- Could improve accuracy beyond 96%

---

## **Complete Understanding Summary:**

### **UVPFL System Overview:**

1. **Architecture:**
   - ResNet50 (pre-trained) + Time Distributed + GRU
   - Input: (30, 120, 240, 3) - 30-frame sequences
   - Federated Learning: Client-side training and storage

2. **Three-Phase Algorithm:**
   - Phase 1: Server-side video processing (segments → frames → tiles)
   - Phase 2: Client-side viewport prediction (ML model + similar user matching)
   - Phase 3: Tile adaptation (hierarchical quality assignment)

3. **Key Components:**
   - User profiling: Per video category (CG fast, NI fast, NI slow)
   - Similar user matching: For cold-start scenarios
   - Viewport merging: When overlap > γ (80%)
   - Tile probability calculation: Equation (1) using angular distributions

4. **Performance:**
   - 96% average accuracy (overall)
   - 86% accuracy (first 7 seconds)
   - Outperforms Mosaic, Flare, Sparkle
   - Best in fast-paced videos (98% for Roller Coaster, Pacman)

5. **Technical Details:**
   - γ threshold: 80% (optimal)
   - Prediction horizons: 1s, 2s, 4s
   - Computational time: 648 ms
   - Model: Adam optimizer, MSE loss, 50 epochs

---

I have a complete understanding of the UVPFL paper. Ready to:
- Review your implementation
- Identify optimization opportunities
- Suggest modifications
- Help with any specific aspects

What would you like to focus on next?

---

**User**

REFERENCES
[1] S. Hollister, “Youtube’s ready to blow your mind with 360-
degree videos,” Mar 2015. [Online]. Available: https://gizmodo.com/
youtubes-ready-to-blow-your-mind-with-360-degree-videos-1690989402
[2] “Global Oculus mobile app new installs 2021 — Statista
— statista.com,” https://www.statista.com/statistics/1283725/
oculus-mobile-app-global-new-installs-christmas/, [Accessed 24-
Jan-2023].
[3] “Cisco annual internet report - cisco annual internet report
(2018–2023) white paper,” Jan 2022. [Online]. Available: https:
//www.cisco.com/c/en/us/solutions/collateral/executive-perspectives/
annual-internet-report/white-paper-c11-741490.html
[4] C. Zhou, Z. Li, and Y. Liu, “A measurement study of oculus 360
degree video streaming,” in Proc. of the 8th ACM on Multimedia
Systems Conference, ser. MMSys’17. New York, USA: ACM, 2017,
p. 27–37. [Online]. Available: https://doi.org/10.1145/3083187.3083190
[5] S. Park, A. Bhattacharya, Z. Yang, S. R. Das, and D. Samaras, “Mosaic:
Advancing user quality of experience in 360-degree video streaming
with machine learning,” IEEE Transactions on Network and Service
Management, vol. 18, no. 1, pp. 1000–1015, 2021.
[6] G.-M. Muntean, G. Ghinea, and T. N. Sheehan, “Region of interest-
based adaptive multimedia streaming scheme,” IEEE Transactions on
Broadcasting, vol. 54, no. 2, pp. 296–303, 2008.
[7] B. Ciubotaru, G.-M. Muntean, and G. Ghinea, “Objective assessment of
region of interest-aware adaptive multimedia streaming quality,” IEEE
Transactions on Broadcasting, vol. 55, no. 2, pp. 202–212, 2009.
[8] A. Yaqoob, T. Bi, and G.-M. Muntean, “A survey on adaptive 360° video
streaming: Solutions, challenges and opportunities,” IEEE Communica-
tions Surveys Tutorials, vol. 22, no. 4, pp. 2801–2838, 2020.
[9] X. Feng, Z. Bao, and S. Wei, “Exploring cnn-based viewport prediction
for live virtual reality streaming,” in 2019 IEEE International Confer-
ence on Artificial Intelligence and Virtual Reality (AIVR), 2019, pp.
183–1833.
Authorized licensed use limited to: Indian Institute Of Technology (Banaras Hindu University) Varanasi. Downloaded on August 12,2025 at 12:49:29 UTC from IEEE Xplore. Restrictions apply.
[10] J. Chen, X. Luo, M. Hu, D. Wu, and Y. Zhou, “Sparkle: User-aware
viewport prediction in 360-degree video streaming,” IEEE Transactions
on Multimedia, vol. 23, pp. 3853–3866, 2021.
[11] X. Feng, Y. Liu, and S. Wei, “Livedeep: Online viewport prediction for
live virtual reality streaming using lifelong deep learning,” in 2020 IEEE
Conference on Virtual Reality and 3D User Interfaces (VR), 2020, pp.
800–808.
[12] A. Yaqoob and G.-M. Muntean, “A combined field-of-view prediction-
assisted viewport adaptive delivery scheme for 360° videos,” IEEE
Transactions on Broadcasting, vol. 67, no. 3, pp. 746–760, 2021.
[13] J. He, M. A. Qureshi, L. Qiu, J. Li, F. Li, and L. Han, “Rubiks:
Practical 360-degree streaming for smartphones,” in Proc. of the 16th
Annual International Conference on Mobile Systems, Applications, and
Services, ser. MobiSys ’18. New York, USA: ACM, 2018, p. 482–494.
[Online]. Available: https://doi.org/10.1145/3210240.3210323
[14] C. Wu, R. Zhang, Z. Wang, and L. Sun, “A spherical convolution
approach for learning long term viewport prediction in 360 immersive
video,” Proceedings of the AAAI Conference on Artificial Intelligence.
[Online]. Available: https://ojs.aaai.org/index.php/AAAI/article/view/
7377
[15] P. Szabo, A. Simiscuka, S. Masneri, M. Zorrilla, and G.-M. Muntean,
“A cnn-based framework for enhancing 360 vr experiences with multi-
sensorial effects,” IEEE Transactions on Multimedia, pp. 1–1, 2022.
[16] F. Qian, B. Han, Q. Xiao, and V. Gopalakrishnan, “Flare: Practical
viewport-adaptive 360-degree video streaming for mobile devices,” in
Proc. of the 24th Annual International Conference on Mobile Computing
and Networking, ser. MobiCom ’18. New York, USA: ACM, 2018, p.
99–114. [Online]. Available: https://doi.org/10.1145/3241539.3241565
[17] X. Che, B. Ip, and L. Lin, “A survey of current youtube video
characteristics,” IEEE MultiMedia, vol. 22, no. 2, pp. 56–63, 2015.
[18] S. Petrangeli, G. Simon, and V. Swaminathan, “Trajectory-based view-
port prediction for 360-degree virtual reality videos,” in 2018 IEEE
International Conference on Artificial Intelligence and Virtual Reality
(AIVR), 2018, pp. 157–160.
[19] A. Dirin, A. Alam ̈aki, and J. Suomala, “Gender differences in per-
ceptions of conventional video, virtual reality and augmented reality,”
International Journal of Interactive Mobile Technologies (iJIM), vol. 13,
06 2019.
[20] F. Needle, “Youtube demographics amp; data to know in 2023
[+ generational patterns],” Aug 2022. [Online]. Available: https:
//blog.hubspot.com/marketing/youtube-demographics
[21] L. Sun, Y. Mao, T. Zong, Y. Liu, and Y. Wang, “Flocking-based live
streaming of 360-degree video,” in Proc. of the 11th ACM Multimedia
Systems Conference, ser. MMSys ’20. New York, USA: ACM, 2020,
p. 26–37. [Online]. Available: https://doi.org/10.1145/3339825.3391856
[22] M. Milon Uddin and J. Park, “360 degree video caching with lru lfu,”
in 2021 IEEE 12th Annual Ubiquitous Computing, Electronics Mobile
Communication Conference (UEMCON), 2021, pp. 0045–0050.
[23] W. Y. B. Lim, N. C. Luong, D. T. Hoang, Y. Jiao, Y.-C. Liang, Q. Yang,
D. Niyato, and C. Miao, “Federated learning in mobile edge networks:
A comprehensive survey,” IEEE Communications Surveys Tutorials,
vol. 22, no. 3, pp. 2031–2063, 2020.
[24] F.-Y. Chao, C. Ozcinar, and A. Smolic, “Privacy-preserving viewport
prediction using federated learning for 360° live video streaming,” in
2022 IEEE 24th International Workshop on Multimedia Signal Process-
ing (MMSP), 2022, pp. 1–6.
[25] S. Chen, D.-L. Xu, and W. Jiang, “High value passenger identification
research based on federated learning,” in 2020 12th International
Conference on Intelligent Human-Machine Systems and Cybernetics
(IHMSC), vol. 1, 2020, pp. 107–110.
[26] Y. Wang, I. L. Bennani, X. Liu, M. Sun, and Y. Zhou, “Electricity
consumer characteristics identification: A federated learning approach,”
IEEE Transactions on Smart Grid, vol. 12, no. 4, pp. 3637–3647, 2021.
[27] P. Zhou, H. Xu, L. H. Lee, P. Fang, and P. Hui, “Are you left
out? an efficient and fair federated learning for personalized profiles
on wearable devices of inferior networking conditions,” Proc. ACM
Interact. Mob. Wearable Ubiquitous Technol., vol. 6, no. 2, jul 2022.
[Online]. Available: https://doi.org/10.1145/3534585
[28] W.-C. Lo, C.-L. Fan, J. Lee, C.-Y. Huang, K.-T. Chen, and C.-H.
Hsu, “360° video viewing dataset in head-mounted virtual reality,”
in Proc. of the 8th ACM on Multimedia Systems Conference, ser.
MMSys’17. New York, USA: ACM, 2017, p. 211–216. [Online].
Available: https://doi.org/10.1145/3083187.3083219
[29] J. Zou, C. Li, C. Liu, Q. Yang, H. Xiong, and E. Steinbach, “Probabilistic
tile visibility-based server-side rate adaptation for adaptive 360-degree
video streaming,” IEEE Journal of Selected Topics in Signal Processing,
vol. 14, no. 1, pp. 161–176, 2020.

---

**Cursor**


## **REFERENCES - Key Papers for Implementation**

### **Critical References:**

1. **[28] - Dataset:**
   - Lo et al., "360° video viewing dataset in head-mounted virtual reality" (MMSys'17)
   - 50 users, 10 videos
   - Primary dataset used in UVPFL experiments

2. **[29] - Tile Probability Equation:**
   - Zou et al., "Probabilistic tile visibility-based server-side rate adaptation"
   - Source of Equation (1) for calculating tile visibility probabilities

3. **SOTA Comparison Methods:**
   - **[5] Mosaic:** Park et al., CNN+LSTM + 3DCNN, 92.21% accuracy
   - **[16] Flare:** Qian et al., Linear/Ridge/SVM, 90.5% (0.2s), 58.2% (1s)
   - **[10] Sparkle:** Chen et al., White box explainable, 94% (1s)

4. **Federated Learning:**
   - **[24] Chao et al.:** Privacy-preserving viewport prediction using FL
   - **[23] Lim et al.:** Comprehensive survey on FL in mobile edge networks

5. **Related Work:**
   - **[9] Feng et al.:** CNN-based viewport prediction (AlexNet, 70-80%)
   - **[11] Feng et al.:** LiveDeep - Online viewport prediction (VGG, 50-90%)
   - **[18] Petrangeli et al.:** Trajectory-based viewport prediction (70%, 50%, 13%)

---

## **Complete Paper Understanding - Summary**

### **UVPFL System Architecture:**

1. **Model:**
   - ResNet50 (pre-trained) → Time Distributed → GRU
   - Input: (30, 120, 240, 3) - 30-frame sequences
   - Output: Predicted viewport (Yaw, Pitch, Roll)

2. **Federated Learning:**
   - Client-side data storage and training
   - User profiling per video category
   - Privacy-preserving approach

3. **Three-Phase Algorithm:**
   - **Phase 1:** Server-side video processing (segments → frames → tiles)
   - **Phase 2:** Client-side viewport prediction (ML + similar user matching)
   - **Phase 3:** Tile adaptation (hierarchical quality)

4. **Key Innovations:**
   - Similar user matching for cold-start
   - Viewport merging when overlap > 80%
   - Tile probability calculation (Equation 1 from [29])
   - Per-category user profiling

5. **Performance:**
   - 96% average accuracy (overall)
   - 86% accuracy (first 7 seconds)
   - Outperforms Mosaic, Flare, Sparkle
   - Best in fast-paced videos (98%)

---

## **Ready for Implementation Review**

I understand:
- The complete UVPFL methodology
- The algorithm phases and flow
- The model architecture and training setup
- The experimental results and comparisons
- The mathematical formulations (Equation 1)
- The dataset structure and video categories

Next steps:
1. Review your current implementation
2. Compare it with the paper's methodology
3. Identify optimization opportunities
4. Suggest modifications or improvements
5. Help debug any issues

Please share:
- Which files you want me to review first
- Any specific issues or areas you want to optimize
- Any questions about aligning your implementation with the paper

Ready to proceed.

---

**User**

@cursor_prepare_for_research_paper_imple234.md go through this file u will understand the process that i went through to implement all of this 

---

**Cursor**


Reviewing the implementation document to understand the process. Reading it in sections.



Continuing to read the implementation sections:



## **Implementation Process Summary**

### **Phase 1: Paper Understanding**
- Paper shared section by section (Abstract → Introduction → Methodology → Experiments → Conclusion)
- Images/figures analyzed (architecture, algorithm, results)
- Dataset identified: NTHU 360° video viewing dataset (50 users, 10 videos)

### **Phase 2: Dataset Setup**
- Dataset downloaded and analyzed
- Structure: `360dataset/` with `content/` (saliency, motion) and `sensory/` (orientation, tiles, raw)
- Preprocessing implemented: separated by user and video category (CG fast-paced, NI fast-paced, NI slow-paced)

### **Phase 3: Implementation Steps**
1. **Step 0**: Environment verification
2. **Step 1**: Data preprocessing (`data_preprocessing.py`)
3. **Step 2**: Data loader (`data_loader.py`) - memory-efficient on-demand loading
4. **Step 3**: Model architecture (`model.py`) - ResNet50 + GRU
5. **Step 4**: Viewport prediction (`viewport_prediction.py`) - similar user matching, viewport merging
6. **Step 5**: Tile adaptation (`tile_adaptation.py`) - hierarchical quality assignment
7. **Step 6**: Training pipeline (`train.py`) - Adam optimizer, MSE loss, 50 epochs

### **Phase 4: Issues Encountered & Resolved**
- GPU license error → CPU fallback implemented
- Storage issues → Cleanup scripts, memory optimization
- HDF5 error on Paramshivay → HDF5 module loading solution
- Memory optimization → Batch size analysis for 8GB/16GB GPUs

### **Phase 5: Documentation**
- Multiple guides created (README, QUICK_START, HOW_TO_RUN, etc.)
- Execution scripts (`run_complete.py`)
- Job scripts for supercomputers (`train_uvpfl.sh`, `test_gpu.sh`)

### **Current Status**
- Core implementation complete
- All paper components implemented
- Ready for training and evaluation
- Federated Learning framework partially implemented

### **Key Implementation Details**
- Model: ResNet50 (frozen) + TimeDistributed + GRU
- Input: (30, 120, 240, 3) - 30-frame sequences
- γ threshold: 80% for viewport merging
- Similar user matching: Cosine similarity on head movement profiles
- Tile probability: Equation (1) from Zou et al.

I understand the implementation. What would you like me to focus on next?
- Optimize specific components
- Fix any issues
- Add missing features
- Improve performance
- Review code quality

---

**User**

understand and explain me the data_preprocessing.py , end to end and add just comments in it in each line for easy understanding

---

**Cursor**


Reviewing `data_preprocessing.py` and adding line-by-line comments.



Explaining `data_preprocessing.py` end-to-end, then adding line-by-line comments.



Explaining `data_preprocessing.py` end-to-end, then adding line-by-line comments.

Summary:
- Purpose: Preprocesses the 360° video dataset per the paper.
- Key steps:
  1. Organize by user (50 users) and video category (CG fast, NI fast, NI slow).
  2. Extract head movement data (Yaw, Pitch, Roll) from CSV files.
  3. Calculate head movement speed.
  4. Create user profiles for Federated Learning.
  5. Save processed data in an organized structure.

Adding detailed comments:


```python
"""
Data Preprocessing for UVPFL - Memory Efficient Version

This script preprocesses the 360-degree video dataset exactly as described in the paper:
1. Separates data for each user
2. Separates data for each video category (CG fast-paced, NI fast-paced, NI slow-paced)
3. Prepares head movement data (Yaw, Pitch, Roll) aligned with frames
4. Creates user profiles for Federated Learning

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- 30 frames per sequence
- Videos are ~60 seconds each at 30 fps = ~1800 frames
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV for video processing (reading video metadata)
import numpy as np  # Numerical computing library for arrays and math operations
import pandas as pd  # Data manipulation library for reading CSV files
from pathlib import Path  # Object-oriented filesystem paths (better than os.path)
from tqdm import tqdm  # Progress bar library for showing processing progress
import json  # JSON encoder/decoder for saving configuration and metadata
import gc  # Garbage collector for memory management (frees memory after processing each video)
from typing import Dict, List, Tuple, Optional  # Type hints for better code documentation

# ============================================================================
# VIDEO CATEGORY MAPPING (From Paper - Figure 7)
# ============================================================================
# Paper states: "We modified the dataset by separating it for each user and video category"
# These categories are used for user profiling in Federated Learning
VIDEO_CATEGORIES = {
    'cg_fast_paced': ['pacman', 'game', 'ride'],  # Computer-Generated fast-paced videos
    'ni_fast_paced': ['coaster', 'coaster2'],  # Natural-Image fast-paced videos
    'ni_slow_paced': ['diving', 'drive', 'landscape', 'panel', 'sport']  # Natural-Image slow-paced videos
}

# Create reverse mapping: video name -> category (for quick lookup)
VIDEO_TO_CATEGORY = {}  # Dictionary to map video name to its category
for category, videos in VIDEO_CATEGORIES.items():  # Iterate through each category
    for video in videos:  # For each video in the category
        VIDEO_TO_CATEGORY[video] = category  # Map video name to category

# Map dataset video names to paper's display names (for readability in output)
VIDEO_NAME_MAPPING = {
    'coaster': 'Roller Coaster',  # Dataset name -> Paper name
    'coaster2': 'Mega Coaster',
    'diving': 'Shark Shipwreck',
    'drive': 'Driving With',
    'game': 'Hog Rider',
    'landscape': 'Kangaroo Island',
    'pacman': 'Pac Man',
    'panel': 'Perils Penal',
    'ride': 'Chariot Race',
    'sport': 'SFR Sport'
}

# Get list of all 10 videos from the dataset
ALL_VIDEOS = list(VIDEO_TO_CATEGORY.keys())  # ['pacman', 'game', 'ride', 'coaster', 'coaster2', ...]

# ============================================================================
# DATASET CONSTANTS (From Paper)
# ============================================================================
NUM_USERS = 50  # Total number of users in the dataset (as per paper)
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification)
CHANNELS = 3  # RGB channels (3 color channels)


class UVPFLDataPreprocessor:
    def __init__(self, dataset_path: str, output_path: str):
        self.dataset_path = Path(dataset_path)
        self.output_path = Path(output_path)
        self.saliency_path = self.dataset_path / 'content' / 'saliency'
        self.orientation_path = self.dataset_path / 'sensory' / 'orientation'
        self.tile_path = self.dataset_path / 'sensory' / 'tile'
        self._create_output_directories()
        self.stats = {'total_frames': 0, 'total_sequences': 0, 'users_processed': 0, 'videos_processed': 0}
    
    def _create_output_directories(self):
        self.output_path.mkdir(parents=True, exist_ok=True)
        for category in VIDEO_CATEGORIES.keys():
            cat_path = self.output_path / category
            cat_path.mkdir(exist_ok=True)
            for video in VIDEO_CATEGORIES[category]:
                (cat_path / video).mkdir(exist_ok=True)
        (self.output_path / 'user_profiles').mkdir(exist_ok=True)
        (self.output_path / 'video_metadata').mkdir(exist_ok=True)
        print(f"Created output directory structure at: {self.output_path}")
    
    def get_video_metadata(self, video_name: str) -> Dict:
        video_path = self.saliency_path / f'{video_name}_saliency.mp4'
        if not video_path.exists():
            return None
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return None
        metadata = {
            'video_name': video_name, 'category': VIDEO_TO_CATEGORY[video_name],
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'saliency_video_path': str(video_path)
        }
        cap.release()
        return metadata
    
    def load_orientation_data(self, video_name: str, user_id: int) -> pd.DataFrame:
        file_path = self.orientation_path / f'{video_name}_user{user_id:02d}_orientation.csv'
        if not file_path.exists():
            return None
        df = pd.read_csv(file_path, skipinitialspace=True)
        df.columns = df.columns.str.strip()
        return df
    
    def load_tile_data(self, video_name: str, user_id: int) -> List[Dict]:
        file_path = self.tile_path / f'{video_name}_user{user_id:02d}_tile.csv'
        if not file_path.exists():
            return None
        tiles_data = []
        with open(file_path, 'r') as f:
            f.readline()
            for line in f:
                parts = line.strip().split(',')
                frame_no = int(parts[0].strip())
                tile_numbers = [int(t.strip()) for t in parts[1:] if t.strip()]
                tiles_data.append({'frame': frame_no, 'tiles': tile_numbers})
        return tiles_data
    
    def calculate_head_movement_speed(self, df: pd.DataFrame) -> np.ndarray:
        yaw, pitch, roll = df['cal. yaw'].values, df['cal. pitch'].values, df['cal. roll'].values
        d_yaw, d_pitch, d_roll = np.diff(yaw, prepend=yaw[0]), np.diff(pitch, prepend=pitch[0]), np.diff(roll, prepend=roll[0])
        return np.sqrt(d_yaw**2 + d_pitch**2 + d_roll**2)
    
    def process_user_video(self, video_name: str, user_id: int) -> Dict:
        df = self.load_orientation_data(video_name, user_id)
        if df is None:
            return None
        tile_data = self.load_tile_data(video_name, user_id)
        speed = self.calculate_head_movement_speed(df)
        category = VIDEO_TO_CATEGORY[video_name]
        num_frames = len(df)
        
        profile = {
            'user_id': user_id, 'video_name': video_name, 'category': category,
            'num_frames': num_frames, 'num_sequences': max(0, num_frames - SEQUENCE_LENGTH),
            'mean_yaw': float(df['cal. yaw'].mean()), 'std_yaw': float(df['cal. yaw'].std()),
            'mean_pitch': float(df['cal. pitch'].mean()), 'std_pitch': float(df['cal. pitch'].std()),
            'mean_roll': float(df['cal. roll'].mean()), 'std_roll': float(df['cal. roll'].std()),
            'mean_speed': float(speed.mean()), 'std_speed': float(speed.std())
        }
        
        orientation_array = np.column_stack([df['cal. yaw'].values, df['cal. pitch'].values, df['cal. roll'].values])
        return {'orientation_array': orientation_array, 'tile_data': tile_data, 'speed': speed, 'profile': profile}
    
    def process_all_data(self):
        print("=" * 60)
        print("UVPFL Data Preprocessing")
        print("=" * 60)
        
        all_profiles = {cat: [] for cat in VIDEO_CATEGORIES.keys()}
        video_metadata = {}
        
        for video_name in tqdm(ALL_VIDEOS, desc="Processing videos"):
            print(f"\nProcessing: {video_name} ({VIDEO_NAME_MAPPING[video_name]})")
            metadata = self.get_video_metadata(video_name)
            if metadata is None:
                continue
            
            video_metadata[video_name] = metadata
            with open(self.output_path / 'video_metadata' / f'{video_name}.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.stats['videos_processed'] += 1
            self.stats['total_frames'] += metadata['frame_count']
            category = VIDEO_TO_CATEGORY[video_name]
            
            for user_id in tqdm(range(1, NUM_USERS + 1), desc=f"Users", leave=False):
                result = self.process_user_video(video_name, user_id)
                if result is None:
                    continue
                
                user_dir = self.output_path / category / video_name / f'user{user_id:02d}'
                user_dir.mkdir(exist_ok=True)
                np.save(user_dir / 'orientation.npy', result['orientation_array'])
                np.save(user_dir / 'speed.npy', result['speed'])
                if result['tile_data']:
                    with open(user_dir / 'tiles.json', 'w') as f:
                        json.dump(result['tile_data'], f)
                with open(user_dir / 'profile.json', 'w') as f:
                    json.dump(result['profile'], f, indent=2)
                
                all_profiles[category].append(result['profile'])
                self.stats['total_sequences'] += result['profile']['num_sequences']
            
            self.stats['users_processed'] += NUM_USERS
            gc.collect()
        
        # Save profiles
        for cat, profiles in all_profiles.items():
            with open(self.output_path / 'user_profiles' / f'{cat}.json', 'w') as f:
                json.dump(profiles, f, indent=2)
        
        # Save metadata
        with open(self.output_path / 'video_metadata' / 'all.json', 'w') as f:
            json.dump(video_metadata, f, indent=2)
        
        config = {
            'video_categories': VIDEO_CATEGORIES, 'video_to_category': VIDEO_TO_CATEGORY,
            'video_name_mapping': VIDEO_NAME_MAPPING, 'all_videos': ALL_VIDEOS,
            'num_users': NUM_USERS, 'sequence_length': SEQUENCE_LENGTH,
            'frame_height': FRAME_HEIGHT, 'frame_width': FRAME_WIDTH
        }
        with open(self.output_path / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        with open(self.output_path / 'stats.json', 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\nDone! Videos: {self.stats['videos_processed']}, Sequences: {self.stats['total_sequences']}")
        return all_profiles
    
    def create_train_test_split(self, test_ratio: float = 0.2, seed: int = 42):
        np.random.seed(seed)
        num_test = int(NUM_USERS * test_ratio)
        all_users = list(range(1, NUM_USERS + 1))
        np.random.shuffle(all_users)
        test_users = sorted(all_users[:num_test])
        train_users = sorted([u for u in range(1, NUM_USERS + 1) if u not in test_users])
        
        split = {'train_users': train_users, 'test_users': test_users, 'seed': seed}
        with open(self.output_path / 'train_test_split.json', 'w') as f:
            json.dump(split, f, indent=2)
        print(f"Train: {len(train_users)}, Test: {len(test_users)}")
        return split


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', default='360dataset')
    parser.add_argument('--output_path', default='processed_data')
    parser.add_argument('--test_ratio', type=float, default=0.2)
    args = parser.parse_args()
    
    preprocessor = UVPFLDataPreprocessor(args.dataset_path, args.output_path)
    preprocessor.process_all_data()
    preprocessor.create_train_test_split(args.test_ratio)


if __name__ == '__main__':
    main()

```

```python
"""
Data Preprocessing for UVPFL - Memory Efficient Version

This script preprocesses the 360-degree video dataset exactly as described in the paper:
1. Separates data for each user
2. Separates data for each video category (CG fast-paced, NI fast-paced, NI slow-paced)
3. Prepares head movement data (Yaw, Pitch, Roll) aligned with frames
4. Creates user profiles for Federated Learning

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- 30 frames per sequence
- Videos are ~60 seconds each at 30 fps = ~1800 frames
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV for video processing (reading video metadata)
import numpy as np  # Numerical computing library for arrays and math operations
import pandas as pd  # Data manipulation library for reading CSV files
from pathlib import Path  # Object-oriented filesystem paths (better than os.path)
from tqdm import tqdm  # Progress bar library for showing processing progress
import json  # JSON encoder/decoder for saving configuration and metadata
import gc  # Garbage collector for memory management (frees memory after processing each video)
from typing import Dict, List, Tuple, Optional  # Type hints for better code documentation

# ============================================================================
# VIDEO CATEGORY MAPPING (From Paper - Figure 7)
# ============================================================================
# Paper states: "We modified the dataset by separating it for each user and video category"
# These categories are used for user profiling in Federated Learning
VIDEO_CATEGORIES = {
    'cg_fast_paced': ['pacman', 'game', 'ride'],  # Computer-Generated fast-paced videos
    'ni_fast_paced': ['coaster', 'coaster2'],  # Natural-Image fast-paced videos
    'ni_slow_paced': ['diving', 'drive', 'landscape', 'panel', 'sport']  # Natural-Image slow-paced videos
}

# Create reverse mapping: video name -> category (for quick lookup)
VIDEO_TO_CATEGORY = {}  # Dictionary to map video name to its category
for category, videos in VIDEO_CATEGORIES.items():  # Iterate through each category
    for video in videos:  # For each video in the category
        VIDEO_TO_CATEGORY[video] = category  # Map video name to category

# Map dataset video names to paper's display names (for readability in output)
VIDEO_NAME_MAPPING = {
    'coaster': 'Roller Coaster',  # Dataset name -> Paper name
    'coaster2': 'Mega Coaster',
    'diving': 'Shark Shipwreck',
    'drive': 'Driving With',
    'game': 'Hog Rider',
    'landscape': 'Kangaroo Island',
    'pacman': 'Pac Man',
    'panel': 'Perils Penal',
    'ride': 'Chariot Race',
    'sport': 'SFR Sport'
}

# Get list of all 10 videos from the dataset
ALL_VIDEOS = list(VIDEO_TO_CATEGORY.keys())  # ['pacman', 'game', 'ride', 'coaster', 'coaster2', ...]

# ============================================================================
# DATASET CONSTANTS (From Paper)
# ============================================================================
NUM_USERS = 50  # Total number of users in the dataset (as per paper)
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification)
CHANNELS = 3  # RGB channels (3 color channels)


# ============================================================================
# UVPFL DATA PREPROCESSOR CLASS
# ============================================================================
class UVPFLDataPreprocessor:
    """
    Main preprocessor class that organizes data by user and video category.
    
    Paper requirement: "We modified the dataset by separating it for each user 
    and video category. This modification helped us test UVPFL approach and get 
    high accuracy for each video and video category separately."
    """
    
    def __init__(self, dataset_path: str, output_path: str):
        """
        Initialize the preprocessor with dataset and output paths.
        
        Args:
            dataset_path: Path to the 360dataset folder (contains content/ and sensory/)
            output_path: Path where processed data will be saved
        """
        self.dataset_path = Path(dataset_path)  # Convert to Path object for easier path operations
        self.output_path = Path(output_path)  # Output directory for processed data
        
        # Define paths to different data folders in the dataset
        self.saliency_path = self.dataset_path / 'content' / 'saliency'  # Saliency video files
        self.orientation_path = self.dataset_path / 'sensory' / 'orientation'  # Head movement CSV files
        self.tile_path = self.dataset_path / 'sensory' / 'tile'  # Tile overlap CSV files
        
        # Create the output directory structure (organized by category and user)
        self._create_output_directories()
        
        # Statistics dictionary to track processing progress
        self.stats = {
            'total_frames': 0,  # Total number of frames processed
            'total_sequences': 0,  # Total number of sequences created (frames - SEQUENCE_LENGTH)
            'users_processed': 0,  # Total number of user-video pairs processed
            'videos_processed': 0  # Number of videos processed
        }
    
    def _create_output_directories(self):
        """
        Create the output directory structure as per paper's methodology.
        
        Structure created:
        processed_data/
        ├── cg_fast_paced/
        │   ├── pacman/
        │   │   ├── user01/
        │   │   ├── user02/
        │   │   └── ...
        │   ├── game/
        │   └── ride/
        ├── ni_fast_paced/
        │   ├── coaster/
        │   └── coaster2/
        ├── ni_slow_paced/
        │   ├── diving/
        │   ├── drive/
        │   └── ...
        ├── user_profiles/  # User profiles for Federated Learning
        └── video_metadata/  # Video metadata (fps, frame count, etc.)
        """
        self.output_path.mkdir(parents=True, exist_ok=True)  # Create main output directory
        
        # Create directories for each video category (CG fast, NI fast, NI slow)
        for category in VIDEO_CATEGORIES.keys():  # Iterate through each category
            cat_path = self.output_path / category  # Path to category folder
            cat_path.mkdir(exist_ok=True)  # Create category directory if it doesn't exist
            
            # Create directories for each video within the category
            for video in VIDEO_CATEGORIES[category]:  # For each video in this category
                (cat_path / video).mkdir(exist_ok=True)  # Create video directory
        
        # Create directories for storing user profiles and video metadata
        (self.output_path / 'user_profiles').mkdir(exist_ok=True)  # For Federated Learning profiles
        (self.output_path / 'video_metadata').mkdir(exist_ok=True)  # For video information
        
        print(f"Created output directory structure at: {self.output_path}")
    
    def get_video_metadata(self, video_name: str) -> Dict:
        video_path = self.saliency_path / f'{video_name}_saliency.mp4'
        if not video_path.exists():
            return None
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return None
        metadata = {
            'video_name': video_name, 'category': VIDEO_TO_CATEGORY[video_name],
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'saliency_video_path': str(video_path)
        }
        cap.release()
        return metadata
    
    def load_orientation_data(self, video_name: str, user_id: int) -> pd.DataFrame:
        file_path = self.orientation_path / f'{video_name}_user{user_id:02d}_orientation.csv'
        if not file_path.exists():
            return None
        df = pd.read_csv(file_path, skipinitialspace=True)
        df.columns = df.columns.str.strip()
        return df
    
    def load_tile_data(self, video_name: str, user_id: int) -> List[Dict]:
        file_path = self.tile_path / f'{video_name}_user{user_id:02d}_tile.csv'
        if not file_path.exists():
            return None
        tiles_data = []
        with open(file_path, 'r') as f:
            f.readline()
            for line in f:
                parts = line.strip().split(',')
                frame_no = int(parts[0].strip())
                tile_numbers = [int(t.strip()) for t in parts[1:] if t.strip()]
                tiles_data.append({'frame': frame_no, 'tiles': tile_numbers})
        return tiles_data
    
    def calculate_head_movement_speed(self, df: pd.DataFrame) -> np.ndarray:
        yaw, pitch, roll = df['cal. yaw'].values, df['cal. pitch'].values, df['cal. roll'].values
        d_yaw, d_pitch, d_roll = np.diff(yaw, prepend=yaw[0]), np.diff(pitch, prepend=pitch[0]), np.diff(roll, prepend=roll[0])
        return np.sqrt(d_yaw**2 + d_pitch**2 + d_roll**2)
    
    def process_user_video(self, video_name: str, user_id: int) -> Dict:
        df = self.load_orientation_data(video_name, user_id)
        if df is None:
            return None
        tile_data = self.load_tile_data(video_name, user_id)
        speed = self.calculate_head_movement_speed(df)
        category = VIDEO_TO_CATEGORY[video_name]
        num_frames = len(df)
        
        profile = {
            'user_id': user_id, 'video_name': video_name, 'category': category,
            'num_frames': num_frames, 'num_sequences': max(0, num_frames - SEQUENCE_LENGTH),
            'mean_yaw': float(df['cal. yaw'].mean()), 'std_yaw': float(df['cal. yaw'].std()),
            'mean_pitch': float(df['cal. pitch'].mean()), 'std_pitch': float(df['cal. pitch'].std()),
            'mean_roll': float(df['cal. roll'].mean()), 'std_roll': float(df['cal. roll'].std()),
            'mean_speed': float(speed.mean()), 'std_speed': float(speed.std())
        }
        
        orientation_array = np.column_stack([df['cal. yaw'].values, df['cal. pitch'].values, df['cal. roll'].values])
        return {'orientation_array': orientation_array, 'tile_data': tile_data, 'speed': speed, 'profile': profile}
    
    def process_all_data(self):
        print("=" * 60)
        print("UVPFL Data Preprocessing")
        print("=" * 60)
        
        all_profiles = {cat: [] for cat in VIDEO_CATEGORIES.keys()}
        video_metadata = {}
        
        for video_name in tqdm(ALL_VIDEOS, desc="Processing videos"):
            print(f"\nProcessing: {video_name} ({VIDEO_NAME_MAPPING[video_name]})")
            metadata = self.get_video_metadata(video_name)
            if metadata is None:
                continue
            
            video_metadata[video_name] = metadata
            with open(self.output_path / 'video_metadata' / f'{video_name}.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.stats['videos_processed'] += 1
            self.stats['total_frames'] += metadata['frame_count']
            category = VIDEO_TO_CATEGORY[video_name]
            
            for user_id in tqdm(range(1, NUM_USERS + 1), desc=f"Users", leave=False):
                result = self.process_user_video(video_name, user_id)
                if result is None:
                    continue
                
                user_dir = self.output_path / category / video_name / f'user{user_id:02d}'
                user_dir.mkdir(exist_ok=True)
                np.save(user_dir / 'orientation.npy', result['orientation_array'])
                np.save(user_dir / 'speed.npy', result['speed'])
                if result['tile_data']:
                    with open(user_dir / 'tiles.json', 'w') as f:
                        json.dump(result['tile_data'], f)
                with open(user_dir / 'profile.json', 'w') as f:
                    json.dump(result['profile'], f, indent=2)
                
                all_profiles[category].append(result['profile'])
                self.stats['total_sequences'] += result['profile']['num_sequences']
            
            self.stats['users_processed'] += NUM_USERS
            gc.collect()
        
        # Save profiles
        for cat, profiles in all_profiles.items():
            with open(self.output_path / 'user_profiles' / f'{cat}.json', 'w') as f:
                json.dump(profiles, f, indent=2)
        
        # Save metadata
        with open(self.output_path / 'video_metadata' / 'all.json', 'w') as f:
            json.dump(video_metadata, f, indent=2)
        
        config = {
            'video_categories': VIDEO_CATEGORIES, 'video_to_category': VIDEO_TO_CATEGORY,
            'video_name_mapping': VIDEO_NAME_MAPPING, 'all_videos': ALL_VIDEOS,
            'num_users': NUM_USERS, 'sequence_length': SEQUENCE_LENGTH,
            'frame_height': FRAME_HEIGHT, 'frame_width': FRAME_WIDTH
        }
        with open(self.output_path / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        with open(self.output_path / 'stats.json', 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\nDone! Videos: {self.stats['videos_processed']}, Sequences: {self.stats['total_sequences']}")
        return all_profiles
    
    def create_train_test_split(self, test_ratio: float = 0.2, seed: int = 42):
        np.random.seed(seed)
        num_test = int(NUM_USERS * test_ratio)
        all_users = list(range(1, NUM_USERS + 1))
        np.random.shuffle(all_users)
        test_users = sorted(all_users[:num_test])
        train_users = sorted([u for u in range(1, NUM_USERS + 1) if u not in test_users])
        
        split = {'train_users': train_users, 'test_users': test_users, 'seed': seed}
        with open(self.output_path / 'train_test_split.json', 'w') as f:
            json.dump(split, f, indent=2)
        print(f"Train: {len(train_users)}, Test: {len(test_users)}")
        return split


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', default='360dataset')
    parser.add_argument('--output_path', default='processed_data')
    parser.add_argument('--test_ratio', type=float, default=0.2)
    args = parser.parse_args()
    
    preprocessor = UVPFLDataPreprocessor(args.dataset_path, args.output_path)
    preprocessor.process_all_data()
    preprocessor.create_train_test_split(args.test_ratio)


if __name__ == '__main__':
    main()

```

```python
"""
Data Preprocessing for UVPFL - Memory Efficient Version

This script preprocesses the 360-degree video dataset exactly as described in the paper:
1. Separates data for each user
2. Separates data for each video category (CG fast-paced, NI fast-paced, NI slow-paced)
3. Prepares head movement data (Yaw, Pitch, Roll) aligned with frames
4. Creates user profiles for Federated Learning

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- 30 frames per sequence
- Videos are ~60 seconds each at 30 fps = ~1800 frames
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV for video processing (reading video metadata)
import numpy as np  # Numerical computing library for arrays and math operations
import pandas as pd  # Data manipulation library for reading CSV files
from pathlib import Path  # Object-oriented filesystem paths (better than os.path)
from tqdm import tqdm  # Progress bar library for showing processing progress
import json  # JSON encoder/decoder for saving configuration and metadata
import gc  # Garbage collector for memory management (frees memory after processing each video)
from typing import Dict, List, Tuple, Optional  # Type hints for better code documentation

# ============================================================================
# VIDEO CATEGORY MAPPING (From Paper - Figure 7)
# ============================================================================
# Paper states: "We modified the dataset by separating it for each user and video category"
# These categories are used for user profiling in Federated Learning
VIDEO_CATEGORIES = {
    'cg_fast_paced': ['pacman', 'game', 'ride'],  # Computer-Generated fast-paced videos
    'ni_fast_paced': ['coaster', 'coaster2'],  # Natural-Image fast-paced videos
    'ni_slow_paced': ['diving', 'drive', 'landscape', 'panel', 'sport']  # Natural-Image slow-paced videos
}

# Create reverse mapping: video name -> category (for quick lookup)
VIDEO_TO_CATEGORY = {}  # Dictionary to map video name to its category
for category, videos in VIDEO_CATEGORIES.items():  # Iterate through each category
    for video in videos:  # For each video in the category
        VIDEO_TO_CATEGORY[video] = category  # Map video name to category

# Map dataset video names to paper's display names (for readability in output)
VIDEO_NAME_MAPPING = {
    'coaster': 'Roller Coaster',  # Dataset name -> Paper name
    'coaster2': 'Mega Coaster',
    'diving': 'Shark Shipwreck',
    'drive': 'Driving With',
    'game': 'Hog Rider',
    'landscape': 'Kangaroo Island',
    'pacman': 'Pac Man',
    'panel': 'Perils Penal',
    'ride': 'Chariot Race',
    'sport': 'SFR Sport'
}

# Get list of all 10 videos from the dataset
ALL_VIDEOS = list(VIDEO_TO_CATEGORY.keys())  # ['pacman', 'game', 'ride', 'coaster', 'coaster2', ...]

# ============================================================================
# DATASET CONSTANTS (From Paper)
# ============================================================================
NUM_USERS = 50  # Total number of users in the dataset (as per paper)
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification)
CHANNELS = 3  # RGB channels (3 color channels)


# ============================================================================
# UVPFL DATA PREPROCESSOR CLASS
# ============================================================================
class UVPFLDataPreprocessor:
    """
    Main preprocessor class that organizes data by user and video category.
    
    Paper requirement: "We modified the dataset by separating it for each user 
    and video category. This modification helped us test UVPFL approach and get 
    high accuracy for each video and video category separately."
    """
    
    def __init__(self, dataset_path: str, output_path: str):
        """
        Initialize the preprocessor with dataset and output paths.
        
        Args:
            dataset_path: Path to the 360dataset folder (contains content/ and sensory/)
            output_path: Path where processed data will be saved
        """
        self.dataset_path = Path(dataset_path)  # Convert to Path object for easier path operations
        self.output_path = Path(output_path)  # Output directory for processed data
        
        # Define paths to different data folders in the dataset
        self.saliency_path = self.dataset_path / 'content' / 'saliency'  # Saliency video files
        self.orientation_path = self.dataset_path / 'sensory' / 'orientation'  # Head movement CSV files
        self.tile_path = self.dataset_path / 'sensory' / 'tile'  # Tile overlap CSV files
        
        # Create the output directory structure (organized by category and user)
        self._create_output_directories()
        
        # Statistics dictionary to track processing progress
        self.stats = {
            'total_frames': 0,  # Total number of frames processed
            'total_sequences': 0,  # Total number of sequences created (frames - SEQUENCE_LENGTH)
            'users_processed': 0,  # Total number of user-video pairs processed
            'videos_processed': 0  # Number of videos processed
        }
    
    def _create_output_directories(self):
        """
        Create the output directory structure as per paper's methodology.
        
        Structure created:
        processed_data/
        ├── cg_fast_paced/
        │   ├── pacman/
        │   │   ├── user01/
        │   │   ├── user02/
        │   │   └── ...
        │   ├── game/
        │   └── ride/
        ├── ni_fast_paced/
        │   ├── coaster/
        │   └── coaster2/
        ├── ni_slow_paced/
        │   ├── diving/
        │   ├── drive/
        │   └── ...
        ├── user_profiles/  # User profiles for Federated Learning
        └── video_metadata/  # Video metadata (fps, frame count, etc.)
        """
        self.output_path.mkdir(parents=True, exist_ok=True)  # Create main output directory
        
        # Create directories for each video category (CG fast, NI fast, NI slow)
        for category in VIDEO_CATEGORIES.keys():  # Iterate through each category
            cat_path = self.output_path / category  # Path to category folder
            cat_path.mkdir(exist_ok=True)  # Create category directory if it doesn't exist
            
            # Create directories for each video within the category
            for video in VIDEO_CATEGORIES[category]:  # For each video in this category
                (cat_path / video).mkdir(exist_ok=True)  # Create video directory
        
        # Create directories for storing user profiles and video metadata
        (self.output_path / 'user_profiles').mkdir(exist_ok=True)  # For Federated Learning profiles
        (self.output_path / 'video_metadata').mkdir(exist_ok=True)  # For video information
        
        print(f"Created output directory structure at: {self.output_path}")
    
    def get_video_metadata(self, video_name: str) -> Dict:
        """
        Extract metadata from saliency video file.
        
        Paper: Videos are ~60 seconds each at 30 fps = ~1800 frames
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Dictionary with video metadata (frame count, fps, dimensions) or None if file not found
        """
        video_path = self.saliency_path / f'{video_name}_saliency.mp4'  # Path to saliency video file
        
        if not video_path.exists():  # Check if video file exists
            return None  # Return None if file not found
        
        cap = cv2.VideoCapture(str(video_path))  # Open video file using OpenCV
        if not cap.isOpened():  # Check if video opened successfully
            return None  # Return None if video couldn't be opened
        
        # Extract video metadata using OpenCV properties
        metadata = {
            'video_name': video_name,  # Video name (e.g., 'coaster')
            'category': VIDEO_TO_CATEGORY[video_name],  # Video category (e.g., 'ni_fast_paced')
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),  # Total number of frames (~1800)
            'fps': cap.get(cv2.CAP_PROP_FPS),  # Frames per second (typically 30)
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  # Video width in pixels
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),  # Video height in pixels
            'saliency_video_path': str(video_path)  # Full path to saliency video
        }
        
        cap.release()  # Release video capture object to free resources
        return metadata  # Return metadata dictionary
    
    def load_orientation_data(self, video_name: str, user_id: int) -> pd.DataFrame:
        """
        Load head movement orientation data for a specific user and video.
        
        Paper: "Yaw (Y), Pitch (PI), and Roll (R) angles are used to calculate 
        the user's current and predicted viewport"
        
        File format: {video_name}_user{user_id:02d}_orientation.csv
        Columns: no. frames, cal. yaw, cal. pitch, cal. roll (calibrated angles)
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            DataFrame with orientation data (Y, PI, R angles per frame) or None if file not found
        """
        # Construct path to orientation CSV file (e.g., 'coaster_user01_orientation.csv')
        file_path = self.orientation_path / f'{video_name}_user{user_id:02d}_orientation.csv'
        
        if not file_path.exists():  # Check if file exists
            return None  # Return None if file not found
        
        # Read CSV file into pandas DataFrame
        df = pd.read_csv(file_path, skipinitialspace=True)  # skipinitialspace removes leading spaces
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
        
        return df  # Return DataFrame with orientation data
    
    def load_tile_data(self, video_name: str, user_id: int) -> List[Dict]:
        """
        Load tile overlap data for a specific user and video.
        
        Paper: "Each frame is further divided into an l×k grid of tiles"
        Tile data shows which tiles overlap with user's Field of View (FoV)
        
        File format: {video_name}_user{user_id:02d}_tile.csv
        Format: frame_number, tile1, tile2, tile3, ... (comma-separated tile IDs)
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            List of dictionaries with frame number and tile IDs, or None if file not found
        """
        # Construct path to tile CSV file (e.g., 'coaster_user01_tile.csv')
        file_path = self.tile_path / f'{video_name}_user{user_id:02d}_tile.csv'
        
        if not file_path.exists():  # Check if file exists
            return None  # Return None if file not found
        
        tiles_data = []  # List to store tile data for each frame
        
        with open(file_path, 'r') as f:  # Open file for reading
            f.readline()  # Skip header line (first line)
            
            for line in f:  # Read each line (each line = one frame)
                parts = line.strip().split(',')  # Split line by comma
                frame_no = int(parts[0].strip())  # First element is frame number
                # Remaining elements are tile numbers (convert to integers, skip empty strings)
                tile_numbers = [int(t.strip()) for t in parts[1:] if t.strip()]
                
                # Store frame number and associated tile IDs
                tiles_data.append({'frame': frame_no, 'tiles': tile_numbers})
        
        return tiles_data  # Return list of tile data dictionaries
    
    def calculate_head_movement_speed(self, df: pd.DataFrame) -> np.ndarray:
        yaw, pitch, roll = df['cal. yaw'].values, df['cal. pitch'].values, df['cal. roll'].values
        d_yaw, d_pitch, d_roll = np.diff(yaw, prepend=yaw[0]), np.diff(pitch, prepend=pitch[0]), np.diff(roll, prepend=roll[0])
        return np.sqrt(d_yaw**2 + d_pitch**2 + d_roll**2)
    
    def process_user_video(self, video_name: str, user_id: int) -> Dict:
        df = self.load_orientation_data(video_name, user_id)
        if df is None:
            return None
        tile_data = self.load_tile_data(video_name, user_id)
        speed = self.calculate_head_movement_speed(df)
        category = VIDEO_TO_CATEGORY[video_name]
        num_frames = len(df)
        
        profile = {
            'user_id': user_id, 'video_name': video_name, 'category': category,
            'num_frames': num_frames, 'num_sequences': max(0, num_frames - SEQUENCE_LENGTH),
            'mean_yaw': float(df['cal. yaw'].mean()), 'std_yaw': float(df['cal. yaw'].std()),
            'mean_pitch': float(df['cal. pitch'].mean()), 'std_pitch': float(df['cal. pitch'].std()),
            'mean_roll': float(df['cal. roll'].mean()), 'std_roll': float(df['cal. roll'].std()),
            'mean_speed': float(speed.mean()), 'std_speed': float(speed.std())
        }
        
        orientation_array = np.column_stack([df['cal. yaw'].values, df['cal. pitch'].values, df['cal. roll'].values])
        return {'orientation_array': orientation_array, 'tile_data': tile_data, 'speed': speed, 'profile': profile}
    
    def process_all_data(self):
        print("=" * 60)
        print("UVPFL Data Preprocessing")
        print("=" * 60)
        
        all_profiles = {cat: [] for cat in VIDEO_CATEGORIES.keys()}
        video_metadata = {}
        
        for video_name in tqdm(ALL_VIDEOS, desc="Processing videos"):
            print(f"\nProcessing: {video_name} ({VIDEO_NAME_MAPPING[video_name]})")
            metadata = self.get_video_metadata(video_name)
            if metadata is None:
                continue
            
            video_metadata[video_name] = metadata
            with open(self.output_path / 'video_metadata' / f'{video_name}.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.stats['videos_processed'] += 1
            self.stats['total_frames'] += metadata['frame_count']
            category = VIDEO_TO_CATEGORY[video_name]
            
            for user_id in tqdm(range(1, NUM_USERS + 1), desc=f"Users", leave=False):
                result = self.process_user_video(video_name, user_id)
                if result is None:
                    continue
                
                user_dir = self.output_path / category / video_name / f'user{user_id:02d}'
                user_dir.mkdir(exist_ok=True)
                np.save(user_dir / 'orientation.npy', result['orientation_array'])
                np.save(user_dir / 'speed.npy', result['speed'])
                if result['tile_data']:
                    with open(user_dir / 'tiles.json', 'w') as f:
                        json.dump(result['tile_data'], f)
                with open(user_dir / 'profile.json', 'w') as f:
                    json.dump(result['profile'], f, indent=2)
                
                all_profiles[category].append(result['profile'])
                self.stats['total_sequences'] += result['profile']['num_sequences']
            
            self.stats['users_processed'] += NUM_USERS
            gc.collect()
        
        # Save profiles
        for cat, profiles in all_profiles.items():
            with open(self.output_path / 'user_profiles' / f'{cat}.json', 'w') as f:
                json.dump(profiles, f, indent=2)
        
        # Save metadata
        with open(self.output_path / 'video_metadata' / 'all.json', 'w') as f:
            json.dump(video_metadata, f, indent=2)
        
        config = {
            'video_categories': VIDEO_CATEGORIES, 'video_to_category': VIDEO_TO_CATEGORY,
            'video_name_mapping': VIDEO_NAME_MAPPING, 'all_videos': ALL_VIDEOS,
            'num_users': NUM_USERS, 'sequence_length': SEQUENCE_LENGTH,
            'frame_height': FRAME_HEIGHT, 'frame_width': FRAME_WIDTH
        }
        with open(self.output_path / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        with open(self.output_path / 'stats.json', 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\nDone! Videos: {self.stats['videos_processed']}, Sequences: {self.stats['total_sequences']}")
        return all_profiles
    
    def create_train_test_split(self, test_ratio: float = 0.2, seed: int = 42):
        np.random.seed(seed)
        num_test = int(NUM_USERS * test_ratio)
        all_users = list(range(1, NUM_USERS + 1))
        np.random.shuffle(all_users)
        test_users = sorted(all_users[:num_test])
        train_users = sorted([u for u in range(1, NUM_USERS + 1) if u not in test_users])
        
        split = {'train_users': train_users, 'test_users': test_users, 'seed': seed}
        with open(self.output_path / 'train_test_split.json', 'w') as f:
            json.dump(split, f, indent=2)
        print(f"Train: {len(train_users)}, Test: {len(test_users)}")
        return split


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', default='360dataset')
    parser.add_argument('--output_path', default='processed_data')
    parser.add_argument('--test_ratio', type=float, default=0.2)
    args = parser.parse_args()
    
    preprocessor = UVPFLDataPreprocessor(args.dataset_path, args.output_path)
    preprocessor.process_all_data()
    preprocessor.create_train_test_split(args.test_ratio)


if __name__ == '__main__':
    main()

```

```python
"""
Data Preprocessing for UVPFL - Memory Efficient Version

This script preprocesses the 360-degree video dataset exactly as described in the paper:
1. Separates data for each user
2. Separates data for each video category (CG fast-paced, NI fast-paced, NI slow-paced)
3. Prepares head movement data (Yaw, Pitch, Roll) aligned with frames
4. Creates user profiles for Federated Learning

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- 30 frames per sequence
- Videos are ~60 seconds each at 30 fps = ~1800 frames
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV for video processing (reading video metadata)
import numpy as np  # Numerical computing library for arrays and math operations
import pandas as pd  # Data manipulation library for reading CSV files
from pathlib import Path  # Object-oriented filesystem paths (better than os.path)
from tqdm import tqdm  # Progress bar library for showing processing progress
import json  # JSON encoder/decoder for saving configuration and metadata
import gc  # Garbage collector for memory management (frees memory after processing each video)
from typing import Dict, List, Tuple, Optional  # Type hints for better code documentation

# ============================================================================
# VIDEO CATEGORY MAPPING (From Paper - Figure 7)
# ============================================================================
# Paper states: "We modified the dataset by separating it for each user and video category"
# These categories are used for user profiling in Federated Learning
VIDEO_CATEGORIES = {
    'cg_fast_paced': ['pacman', 'game', 'ride'],  # Computer-Generated fast-paced videos
    'ni_fast_paced': ['coaster', 'coaster2'],  # Natural-Image fast-paced videos
    'ni_slow_paced': ['diving', 'drive', 'landscape', 'panel', 'sport']  # Natural-Image slow-paced videos
}

# Create reverse mapping: video name -> category (for quick lookup)
VIDEO_TO_CATEGORY = {}  # Dictionary to map video name to its category
for category, videos in VIDEO_CATEGORIES.items():  # Iterate through each category
    for video in videos:  # For each video in the category
        VIDEO_TO_CATEGORY[video] = category  # Map video name to category

# Map dataset video names to paper's display names (for readability in output)
VIDEO_NAME_MAPPING = {
    'coaster': 'Roller Coaster',  # Dataset name -> Paper name
    'coaster2': 'Mega Coaster',
    'diving': 'Shark Shipwreck',
    'drive': 'Driving With',
    'game': 'Hog Rider',
    'landscape': 'Kangaroo Island',
    'pacman': 'Pac Man',
    'panel': 'Perils Penal',
    'ride': 'Chariot Race',
    'sport': 'SFR Sport'
}

# Get list of all 10 videos from the dataset
ALL_VIDEOS = list(VIDEO_TO_CATEGORY.keys())  # ['pacman', 'game', 'ride', 'coaster', 'coaster2', ...]

# ============================================================================
# DATASET CONSTANTS (From Paper)
# ============================================================================
NUM_USERS = 50  # Total number of users in the dataset (as per paper)
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification)
CHANNELS = 3  # RGB channels (3 color channels)


# ============================================================================
# UVPFL DATA PREPROCESSOR CLASS
# ============================================================================
class UVPFLDataPreprocessor:
    """
    Main preprocessor class that organizes data by user and video category.
    
    Paper requirement: "We modified the dataset by separating it for each user 
    and video category. This modification helped us test UVPFL approach and get 
    high accuracy for each video and video category separately."
    """
    
    def __init__(self, dataset_path: str, output_path: str):
        """
        Initialize the preprocessor with dataset and output paths.
        
        Args:
            dataset_path: Path to the 360dataset folder (contains content/ and sensory/)
            output_path: Path where processed data will be saved
        """
        self.dataset_path = Path(dataset_path)  # Convert to Path object for easier path operations
        self.output_path = Path(output_path)  # Output directory for processed data
        
        # Define paths to different data folders in the dataset
        self.saliency_path = self.dataset_path / 'content' / 'saliency'  # Saliency video files
        self.orientation_path = self.dataset_path / 'sensory' / 'orientation'  # Head movement CSV files
        self.tile_path = self.dataset_path / 'sensory' / 'tile'  # Tile overlap CSV files
        
        # Create the output directory structure (organized by category and user)
        self._create_output_directories()
        
        # Statistics dictionary to track processing progress
        self.stats = {
            'total_frames': 0,  # Total number of frames processed
            'total_sequences': 0,  # Total number of sequences created (frames - SEQUENCE_LENGTH)
            'users_processed': 0,  # Total number of user-video pairs processed
            'videos_processed': 0  # Number of videos processed
        }
    
    def _create_output_directories(self):
        """
        Create the output directory structure as per paper's methodology.
        
        Structure created:
        processed_data/
        ├── cg_fast_paced/
        │   ├── pacman/
        │   │   ├── user01/
        │   │   ├── user02/
        │   │   └── ...
        │   ├── game/
        │   └── ride/
        ├── ni_fast_paced/
        │   ├── coaster/
        │   └── coaster2/
        ├── ni_slow_paced/
        │   ├── diving/
        │   ├── drive/
        │   └── ...
        ├── user_profiles/  # User profiles for Federated Learning
        └── video_metadata/  # Video metadata (fps, frame count, etc.)
        """
        self.output_path.mkdir(parents=True, exist_ok=True)  # Create main output directory
        
        # Create directories for each video category (CG fast, NI fast, NI slow)
        for category in VIDEO_CATEGORIES.keys():  # Iterate through each category
            cat_path = self.output_path / category  # Path to category folder
            cat_path.mkdir(exist_ok=True)  # Create category directory if it doesn't exist
            
            # Create directories for each video within the category
            for video in VIDEO_CATEGORIES[category]:  # For each video in this category
                (cat_path / video).mkdir(exist_ok=True)  # Create video directory
        
        # Create directories for storing user profiles and video metadata
        (self.output_path / 'user_profiles').mkdir(exist_ok=True)  # For Federated Learning profiles
        (self.output_path / 'video_metadata').mkdir(exist_ok=True)  # For video information
        
        print(f"Created output directory structure at: {self.output_path}")
    
    def get_video_metadata(self, video_name: str) -> Dict:
        """
        Extract metadata from saliency video file.
        
        Paper: Videos are ~60 seconds each at 30 fps = ~1800 frames
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Dictionary with video metadata (frame count, fps, dimensions) or None if file not found
        """
        video_path = self.saliency_path / f'{video_name}_saliency.mp4'  # Path to saliency video file
        
        if not video_path.exists():  # Check if video file exists
            return None  # Return None if file not found
        
        cap = cv2.VideoCapture(str(video_path))  # Open video file using OpenCV
        if not cap.isOpened():  # Check if video opened successfully
            return None  # Return None if video couldn't be opened
        
        # Extract video metadata using OpenCV properties
        metadata = {
            'video_name': video_name,  # Video name (e.g., 'coaster')
            'category': VIDEO_TO_CATEGORY[video_name],  # Video category (e.g., 'ni_fast_paced')
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),  # Total number of frames (~1800)
            'fps': cap.get(cv2.CAP_PROP_FPS),  # Frames per second (typically 30)
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  # Video width in pixels
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),  # Video height in pixels
            'saliency_video_path': str(video_path)  # Full path to saliency video
        }
        
        cap.release()  # Release video capture object to free resources
        return metadata  # Return metadata dictionary
    
    def load_orientation_data(self, video_name: str, user_id: int) -> pd.DataFrame:
        """
        Load head movement orientation data for a specific user and video.
        
        Paper: "Yaw (Y), Pitch (PI), and Roll (R) angles are used to calculate 
        the user's current and predicted viewport"
        
        File format: {video_name}_user{user_id:02d}_orientation.csv
        Columns: no. frames, cal. yaw, cal. pitch, cal. roll (calibrated angles)
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            DataFrame with orientation data (Y, PI, R angles per frame) or None if file not found
        """
        # Construct path to orientation CSV file (e.g., 'coaster_user01_orientation.csv')
        file_path = self.orientation_path / f'{video_name}_user{user_id:02d}_orientation.csv'
        
        if not file_path.exists():  # Check if file exists
            return None  # Return None if file not found
        
        # Read CSV file into pandas DataFrame
        df = pd.read_csv(file_path, skipinitialspace=True)  # skipinitialspace removes leading spaces
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
        
        return df  # Return DataFrame with orientation data
    
    def load_tile_data(self, video_name: str, user_id: int) -> List[Dict]:
        """
        Load tile overlap data for a specific user and video.
        
        Paper: "Each frame is further divided into an l×k grid of tiles"
        Tile data shows which tiles overlap with user's Field of View (FoV)
        
        File format: {video_name}_user{user_id:02d}_tile.csv
        Format: frame_number, tile1, tile2, tile3, ... (comma-separated tile IDs)
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            List of dictionaries with frame number and tile IDs, or None if file not found
        """
        # Construct path to tile CSV file (e.g., 'coaster_user01_tile.csv')
        file_path = self.tile_path / f'{video_name}_user{user_id:02d}_tile.csv'
        
        if not file_path.exists():  # Check if file exists
            return None  # Return None if file not found
        
        tiles_data = []  # List to store tile data for each frame
        
        with open(file_path, 'r') as f:  # Open file for reading
            f.readline()  # Skip header line (first line)
            
            for line in f:  # Read each line (each line = one frame)
                parts = line.strip().split(',')  # Split line by comma
                frame_no = int(parts[0].strip())  # First element is frame number
                # Remaining elements are tile numbers (convert to integers, skip empty strings)
                tile_numbers = [int(t.strip()) for t in parts[1:] if t.strip()]
                
                # Store frame number and associated tile IDs
                tiles_data.append({'frame': frame_no, 'tiles': tile_numbers})
        
        return tiles_data  # Return list of tile data dictionaries
    
    def calculate_head_movement_speed(self, df: pd.DataFrame) -> np.ndarray:
        """
        Calculate head movement speed from orientation data.
        
        Paper: "Calculate head movement speed of User" (Algorithm 1, Phase 2)
        
        Speed is calculated as the magnitude of angular velocity:
        speed = sqrt(Δyaw² + Δpitch² + Δroll²)
        This represents how fast the user's head is moving in 3D space.
        
        Args:
            df: DataFrame with orientation data (columns: 'cal. yaw', 'cal. pitch', 'cal. roll')
            
        Returns:
            NumPy array of head movement speeds (one value per frame)
        """
        # Extract Yaw (Y), Pitch (PI), and Roll (R) angles as NumPy arrays
        yaw = df['cal. yaw'].values  # Horizontal rotation angles (degrees)
        pitch = df['cal. pitch'].values  # Vertical rotation angles (degrees)
        roll = df['cal. roll'].values  # Tilt angles (degrees)
        
        # Calculate angular velocity (change in angles between consecutive frames)
        # np.diff calculates difference: [a, b, c] -> [b-a, c-b]
        # prepend adds first value at beginning so arrays have same length
        d_yaw = np.diff(yaw, prepend=yaw[0])  # Change in yaw per frame
        d_pitch = np.diff(pitch, prepend=pitch[0])  # Change in pitch per frame
        d_roll = np.diff(roll, prepend=roll[0])  # Change in roll per frame
        
        # Calculate speed as magnitude of 3D angular velocity vector
        # This gives us how fast the head is moving overall
        return np.sqrt(d_yaw**2 + d_pitch**2 + d_roll**2)  # Euclidean distance in 3D angle space
    
    def process_user_video(self, video_name: str, user_id: int) -> Dict:
        """
        Process data for a single user-video pair.
        
        This is the core processing function that:
        1. Loads orientation data (Y, PI, R)
        2. Loads tile data
        3. Calculates head movement speed
        4. Creates user profile for Federated Learning
        
        Paper: "UVPFL profiles users based on their head movements for different 
        categories of videos"
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            Dictionary containing:
            - orientation_array: NumPy array of (Y, PI, R) angles per frame
            - tile_data: List of tile overlap data
            - speed: Head movement speed array
            - profile: User profile dictionary for similarity matching
        """
        # Load orientation data (head movement angles) for this user-video pair
        df = self.load_orientation_data(video_name, user_id)
        if df is None:  # If file not found, skip this user-video pair
            return None
        
        # Load tile data (which tiles overlap with user's viewport)
        tile_data = self.load_tile_data(video_name, user_id)
        
        # Calculate head movement speed (used in user profiling)
        speed = self.calculate_head_movement_speed(df)
        
        # Get video category (for organizing data and user profiling)
        category = VIDEO_TO_CATEGORY[video_name]  # e.g., 'ni_fast_paced'
        
        # Get number of frames in this video for this user
        num_frames = len(df)  # Typically ~1800 frames (60 seconds * 30 fps)
        
        # Create user profile for Federated Learning and similarity matching
        # Paper: "UVPFL profiles users based on their head movements for different 
        # categories of videos"
        profile = {
            'user_id': user_id,  # User identifier (1-50)
            'video_name': video_name,  # Video name (e.g., 'coaster')
            'category': category,  # Video category (e.g., 'ni_fast_paced')
            'num_frames': num_frames,  # Total frames for this user-video pair
            # Number of sequences that can be created (sliding window of 30 frames)
            'num_sequences': max(0, num_frames - SEQUENCE_LENGTH),
            # Statistical features for similarity matching (mean and std of each angle)
            'mean_yaw': float(df['cal. yaw'].mean()),  # Average yaw angle
            'std_yaw': float(df['cal. yaw'].std()),  # Standard deviation of yaw
            'mean_pitch': float(df['cal. pitch'].mean()),  # Average pitch angle
            'std_pitch': float(df['cal. pitch'].std()),  # Standard deviation of pitch
            'mean_roll': float(df['cal. roll'].mean()),  # Average roll angle
            'std_roll': float(df['cal. roll'].std()),  # Standard deviation of roll
            'mean_speed': float(speed.mean()),  # Average head movement speed
            'std_speed': float(speed.std())  # Standard deviation of speed
        }
        
        # Create NumPy array of orientation angles (Y, PI, R) for each frame
        # Shape: (num_frames, 3) where columns are [yaw, pitch, roll]
        # This will be used as target data for model training
        orientation_array = np.column_stack([
            df['cal. yaw'].values,  # Yaw angles
            df['cal. pitch'].values,  # Pitch angles
            df['cal. roll'].values  # Roll angles
        ])
        
        # Return all processed data for this user-video pair
        return {
            'orientation_array': orientation_array,  # (num_frames, 3) array of angles
            'tile_data': tile_data,  # List of tile overlap data
            'speed': speed,  # Head movement speed array
            'profile': profile  # User profile for Federated Learning
        }
    
    def process_all_data(self):
        print("=" * 60)
        print("UVPFL Data Preprocessing")
        print("=" * 60)
        
        all_profiles = {cat: [] for cat in VIDEO_CATEGORIES.keys()}
        video_metadata = {}
        
        for video_name in tqdm(ALL_VIDEOS, desc="Processing videos"):
            print(f"\nProcessing: {video_name} ({VIDEO_NAME_MAPPING[video_name]})")
            metadata = self.get_video_metadata(video_name)
            if metadata is None:
                continue
            
            video_metadata[video_name] = metadata
            with open(self.output_path / 'video_metadata' / f'{video_name}.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.stats['videos_processed'] += 1
            self.stats['total_frames'] += metadata['frame_count']
            category = VIDEO_TO_CATEGORY[video_name]
            
            for user_id in tqdm(range(1, NUM_USERS + 1), desc=f"Users", leave=False):
                result = self.process_user_video(video_name, user_id)
                if result is None:
                    continue
                
                user_dir = self.output_path / category / video_name / f'user{user_id:02d}'
                user_dir.mkdir(exist_ok=True)
                np.save(user_dir / 'orientation.npy', result['orientation_array'])
                np.save(user_dir / 'speed.npy', result['speed'])
                if result['tile_data']:
                    with open(user_dir / 'tiles.json', 'w') as f:
                        json.dump(result['tile_data'], f)
                with open(user_dir / 'profile.json', 'w') as f:
                    json.dump(result['profile'], f, indent=2)
                
                all_profiles[category].append(result['profile'])
                self.stats['total_sequences'] += result['profile']['num_sequences']
            
            self.stats['users_processed'] += NUM_USERS
            gc.collect()
        
        # Save profiles
        for cat, profiles in all_profiles.items():
            with open(self.output_path / 'user_profiles' / f'{cat}.json', 'w') as f:
                json.dump(profiles, f, indent=2)
        
        # Save metadata
        with open(self.output_path / 'video_metadata' / 'all.json', 'w') as f:
            json.dump(video_metadata, f, indent=2)
        
        config = {
            'video_categories': VIDEO_CATEGORIES, 'video_to_category': VIDEO_TO_CATEGORY,
            'video_name_mapping': VIDEO_NAME_MAPPING, 'all_videos': ALL_VIDEOS,
            'num_users': NUM_USERS, 'sequence_length': SEQUENCE_LENGTH,
            'frame_height': FRAME_HEIGHT, 'frame_width': FRAME_WIDTH
        }
        with open(self.output_path / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        with open(self.output_path / 'stats.json', 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\nDone! Videos: {self.stats['videos_processed']}, Sequences: {self.stats['total_sequences']}")
        return all_profiles
    
    def create_train_test_split(self, test_ratio: float = 0.2, seed: int = 42):
        np.random.seed(seed)
        num_test = int(NUM_USERS * test_ratio)
        all_users = list(range(1, NUM_USERS + 1))
        np.random.shuffle(all_users)
        test_users = sorted(all_users[:num_test])
        train_users = sorted([u for u in range(1, NUM_USERS + 1) if u not in test_users])
        
        split = {'train_users': train_users, 'test_users': test_users, 'seed': seed}
        with open(self.output_path / 'train_test_split.json', 'w') as f:
            json.dump(split, f, indent=2)
        print(f"Train: {len(train_users)}, Test: {len(test_users)}")
        return split


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', default='360dataset')
    parser.add_argument('--output_path', default='processed_data')
    parser.add_argument('--test_ratio', type=float, default=0.2)
    args = parser.parse_args()
    
    preprocessor = UVPFLDataPreprocessor(args.dataset_path, args.output_path)
    preprocessor.process_all_data()
    preprocessor.create_train_test_split(args.test_ratio)


if __name__ == '__main__':
    main()

```

```python
"""
Data Preprocessing for UVPFL - Memory Efficient Version

This script preprocesses the 360-degree video dataset exactly as described in the paper:
1. Separates data for each user
2. Separates data for each video category (CG fast-paced, NI fast-paced, NI slow-paced)
3. Prepares head movement data (Yaw, Pitch, Roll) aligned with frames
4. Creates user profiles for Federated Learning

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- 30 frames per sequence
- Videos are ~60 seconds each at 30 fps = ~1800 frames
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV for video processing (reading video metadata)
import numpy as np  # Numerical computing library for arrays and math operations
import pandas as pd  # Data manipulation library for reading CSV files
from pathlib import Path  # Object-oriented filesystem paths (better than os.path)
from tqdm import tqdm  # Progress bar library for showing processing progress
import json  # JSON encoder/decoder for saving configuration and metadata
import gc  # Garbage collector for memory management (frees memory after processing each video)
from typing import Dict, List, Tuple, Optional  # Type hints for better code documentation

# ============================================================================
# VIDEO CATEGORY MAPPING (From Paper - Figure 7)
# ============================================================================
# Paper states: "We modified the dataset by separating it for each user and video category"
# These categories are used for user profiling in Federated Learning
VIDEO_CATEGORIES = {
    'cg_fast_paced': ['pacman', 'game', 'ride'],  # Computer-Generated fast-paced videos
    'ni_fast_paced': ['coaster', 'coaster2'],  # Natural-Image fast-paced videos
    'ni_slow_paced': ['diving', 'drive', 'landscape', 'panel', 'sport']  # Natural-Image slow-paced videos
}

# Create reverse mapping: video name -> category (for quick lookup)
VIDEO_TO_CATEGORY = {}  # Dictionary to map video name to its category
for category, videos in VIDEO_CATEGORIES.items():  # Iterate through each category
    for video in videos:  # For each video in the category
        VIDEO_TO_CATEGORY[video] = category  # Map video name to category

# Map dataset video names to paper's display names (for readability in output)
VIDEO_NAME_MAPPING = {
    'coaster': 'Roller Coaster',  # Dataset name -> Paper name
    'coaster2': 'Mega Coaster',
    'diving': 'Shark Shipwreck',
    'drive': 'Driving With',
    'game': 'Hog Rider',
    'landscape': 'Kangaroo Island',
    'pacman': 'Pac Man',
    'panel': 'Perils Penal',
    'ride': 'Chariot Race',
    'sport': 'SFR Sport'
}

# Get list of all 10 videos from the dataset
ALL_VIDEOS = list(VIDEO_TO_CATEGORY.keys())  # ['pacman', 'game', 'ride', 'coaster', 'coaster2', ...]

# ============================================================================
# DATASET CONSTANTS (From Paper)
# ============================================================================
NUM_USERS = 50  # Total number of users in the dataset (as per paper)
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification)
CHANNELS = 3  # RGB channels (3 color channels)


# ============================================================================
# UVPFL DATA PREPROCESSOR CLASS
# ============================================================================
class UVPFLDataPreprocessor:
    """
    Main preprocessor class that organizes data by user and video category.
    
    Paper requirement: "We modified the dataset by separating it for each user 
    and video category. This modification helped us test UVPFL approach and get 
    high accuracy for each video and video category separately."
    """
    
    def __init__(self, dataset_path: str, output_path: str):
        """
        Initialize the preprocessor with dataset and output paths.
        
        Args:
            dataset_path: Path to the 360dataset folder (contains content/ and sensory/)
            output_path: Path where processed data will be saved
        """
        self.dataset_path = Path(dataset_path)  # Convert to Path object for easier path operations
        self.output_path = Path(output_path)  # Output directory for processed data
        
        # Define paths to different data folders in the dataset
        self.saliency_path = self.dataset_path / 'content' / 'saliency'  # Saliency video files
        self.orientation_path = self.dataset_path / 'sensory' / 'orientation'  # Head movement CSV files
        self.tile_path = self.dataset_path / 'sensory' / 'tile'  # Tile overlap CSV files
        
        # Create the output directory structure (organized by category and user)
        self._create_output_directories()
        
        # Statistics dictionary to track processing progress
        self.stats = {
            'total_frames': 0,  # Total number of frames processed
            'total_sequences': 0,  # Total number of sequences created (frames - SEQUENCE_LENGTH)
            'users_processed': 0,  # Total number of user-video pairs processed
            'videos_processed': 0  # Number of videos processed
        }
    
    def _create_output_directories(self):
        """
        Create the output directory structure as per paper's methodology.
        
        Structure created:
        processed_data/
        ├── cg_fast_paced/
        │   ├── pacman/
        │   │   ├── user01/
        │   │   ├── user02/
        │   │   └── ...
        │   ├── game/
        │   └── ride/
        ├── ni_fast_paced/
        │   ├── coaster/
        │   └── coaster2/
        ├── ni_slow_paced/
        │   ├── diving/
        │   ├── drive/
        │   └── ...
        ├── user_profiles/  # User profiles for Federated Learning
        └── video_metadata/  # Video metadata (fps, frame count, etc.)
        """
        self.output_path.mkdir(parents=True, exist_ok=True)  # Create main output directory
        
        # Create directories for each video category (CG fast, NI fast, NI slow)
        for category in VIDEO_CATEGORIES.keys():  # Iterate through each category
            cat_path = self.output_path / category  # Path to category folder
            cat_path.mkdir(exist_ok=True)  # Create category directory if it doesn't exist
            
            # Create directories for each video within the category
            for video in VIDEO_CATEGORIES[category]:  # For each video in this category
                (cat_path / video).mkdir(exist_ok=True)  # Create video directory
        
        # Create directories for storing user profiles and video metadata
        (self.output_path / 'user_profiles').mkdir(exist_ok=True)  # For Federated Learning profiles
        (self.output_path / 'video_metadata').mkdir(exist_ok=True)  # For video information
        
        print(f"Created output directory structure at: {self.output_path}")
    
    def get_video_metadata(self, video_name: str) -> Dict:
        """
        Extract metadata from saliency video file.
        
        Paper: Videos are ~60 seconds each at 30 fps = ~1800 frames
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Dictionary with video metadata (frame count, fps, dimensions) or None if file not found
        """
        video_path = self.saliency_path / f'{video_name}_saliency.mp4'  # Path to saliency video file
        
        if not video_path.exists():  # Check if video file exists
            return None  # Return None if file not found
        
        cap = cv2.VideoCapture(str(video_path))  # Open video file using OpenCV
        if not cap.isOpened():  # Check if video opened successfully
            return None  # Return None if video couldn't be opened
        
        # Extract video metadata using OpenCV properties
        metadata = {
            'video_name': video_name,  # Video name (e.g., 'coaster')
            'category': VIDEO_TO_CATEGORY[video_name],  # Video category (e.g., 'ni_fast_paced')
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),  # Total number of frames (~1800)
            'fps': cap.get(cv2.CAP_PROP_FPS),  # Frames per second (typically 30)
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  # Video width in pixels
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),  # Video height in pixels
            'saliency_video_path': str(video_path)  # Full path to saliency video
        }
        
        cap.release()  # Release video capture object to free resources
        return metadata  # Return metadata dictionary
    
    def load_orientation_data(self, video_name: str, user_id: int) -> pd.DataFrame:
        """
        Load head movement orientation data for a specific user and video.
        
        Paper: "Yaw (Y), Pitch (PI), and Roll (R) angles are used to calculate 
        the user's current and predicted viewport"
        
        File format: {video_name}_user{user_id:02d}_orientation.csv
        Columns: no. frames, cal. yaw, cal. pitch, cal. roll (calibrated angles)
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            DataFrame with orientation data (Y, PI, R angles per frame) or None if file not found
        """
        # Construct path to orientation CSV file (e.g., 'coaster_user01_orientation.csv')
        file_path = self.orientation_path / f'{video_name}_user{user_id:02d}_orientation.csv'
        
        if not file_path.exists():  # Check if file exists
            return None  # Return None if file not found
        
        # Read CSV file into pandas DataFrame
        df = pd.read_csv(file_path, skipinitialspace=True)  # skipinitialspace removes leading spaces
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
        
        return df  # Return DataFrame with orientation data
    
    def load_tile_data(self, video_name: str, user_id: int) -> List[Dict]:
        """
        Load tile overlap data for a specific user and video.
        
        Paper: "Each frame is further divided into an l×k grid of tiles"
        Tile data shows which tiles overlap with user's Field of View (FoV)
        
        File format: {video_name}_user{user_id:02d}_tile.csv
        Format: frame_number, tile1, tile2, tile3, ... (comma-separated tile IDs)
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            List of dictionaries with frame number and tile IDs, or None if file not found
        """
        # Construct path to tile CSV file (e.g., 'coaster_user01_tile.csv')
        file_path = self.tile_path / f'{video_name}_user{user_id:02d}_tile.csv'
        
        if not file_path.exists():  # Check if file exists
            return None  # Return None if file not found
        
        tiles_data = []  # List to store tile data for each frame
        
        with open(file_path, 'r') as f:  # Open file for reading
            f.readline()  # Skip header line (first line)
            
            for line in f:  # Read each line (each line = one frame)
                parts = line.strip().split(',')  # Split line by comma
                frame_no = int(parts[0].strip())  # First element is frame number
                # Remaining elements are tile numbers (convert to integers, skip empty strings)
                tile_numbers = [int(t.strip()) for t in parts[1:] if t.strip()]
                
                # Store frame number and associated tile IDs
                tiles_data.append({'frame': frame_no, 'tiles': tile_numbers})
        
        return tiles_data  # Return list of tile data dictionaries
    
    def calculate_head_movement_speed(self, df: pd.DataFrame) -> np.ndarray:
        """
        Calculate head movement speed from orientation data.
        
        Paper: "Calculate head movement speed of User" (Algorithm 1, Phase 2)
        
        Speed is calculated as the magnitude of angular velocity:
        speed = sqrt(Δyaw² + Δpitch² + Δroll²)
        This represents how fast the user's head is moving in 3D space.
        
        Args:
            df: DataFrame with orientation data (columns: 'cal. yaw', 'cal. pitch', 'cal. roll')
            
        Returns:
            NumPy array of head movement speeds (one value per frame)
        """
        # Extract Yaw (Y), Pitch (PI), and Roll (R) angles as NumPy arrays
        yaw = df['cal. yaw'].values  # Horizontal rotation angles (degrees)
        pitch = df['cal. pitch'].values  # Vertical rotation angles (degrees)
        roll = df['cal. roll'].values  # Tilt angles (degrees)
        
        # Calculate angular velocity (change in angles between consecutive frames)
        # np.diff calculates difference: [a, b, c] -> [b-a, c-b]
        # prepend adds first value at beginning so arrays have same length
        d_yaw = np.diff(yaw, prepend=yaw[0])  # Change in yaw per frame
        d_pitch = np.diff(pitch, prepend=pitch[0])  # Change in pitch per frame
        d_roll = np.diff(roll, prepend=roll[0])  # Change in roll per frame
        
        # Calculate speed as magnitude of 3D angular velocity vector
        # This gives us how fast the head is moving overall
        return np.sqrt(d_yaw**2 + d_pitch**2 + d_roll**2)  # Euclidean distance in 3D angle space
    
    def process_user_video(self, video_name: str, user_id: int) -> Dict:
        """
        Process data for a single user-video pair.
        
        This is the core processing function that:
        1. Loads orientation data (Y, PI, R)
        2. Loads tile data
        3. Calculates head movement speed
        4. Creates user profile for Federated Learning
        
        Paper: "UVPFL profiles users based on their head movements for different 
        categories of videos"
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            Dictionary containing:
            - orientation_array: NumPy array of (Y, PI, R) angles per frame
            - tile_data: List of tile overlap data
            - speed: Head movement speed array
            - profile: User profile dictionary for similarity matching
        """
        # Load orientation data (head movement angles) for this user-video pair
        df = self.load_orientation_data(video_name, user_id)
        if df is None:  # If file not found, skip this user-video pair
            return None
        
        # Load tile data (which tiles overlap with user's viewport)
        tile_data = self.load_tile_data(video_name, user_id)
        
        # Calculate head movement speed (used in user profiling)
        speed = self.calculate_head_movement_speed(df)
        
        # Get video category (for organizing data and user profiling)
        category = VIDEO_TO_CATEGORY[video_name]  # e.g., 'ni_fast_paced'
        
        # Get number of frames in this video for this user
        num_frames = len(df)  # Typically ~1800 frames (60 seconds * 30 fps)
        
        # Create user profile for Federated Learning and similarity matching
        # Paper: "UVPFL profiles users based on their head movements for different 
        # categories of videos"
        profile = {
            'user_id': user_id,  # User identifier (1-50)
            'video_name': video_name,  # Video name (e.g., 'coaster')
            'category': category,  # Video category (e.g., 'ni_fast_paced')
            'num_frames': num_frames,  # Total frames for this user-video pair
            # Number of sequences that can be created (sliding window of 30 frames)
            'num_sequences': max(0, num_frames - SEQUENCE_LENGTH),
            # Statistical features for similarity matching (mean and std of each angle)
            'mean_yaw': float(df['cal. yaw'].mean()),  # Average yaw angle
            'std_yaw': float(df['cal. yaw'].std()),  # Standard deviation of yaw
            'mean_pitch': float(df['cal. pitch'].mean()),  # Average pitch angle
            'std_pitch': float(df['cal. pitch'].std()),  # Standard deviation of pitch
            'mean_roll': float(df['cal. roll'].mean()),  # Average roll angle
            'std_roll': float(df['cal. roll'].std()),  # Standard deviation of roll
            'mean_speed': float(speed.mean()),  # Average head movement speed
            'std_speed': float(speed.std())  # Standard deviation of speed
        }
        
        # Create NumPy array of orientation angles (Y, PI, R) for each frame
        # Shape: (num_frames, 3) where columns are [yaw, pitch, roll]
        # This will be used as target data for model training
        orientation_array = np.column_stack([
            df['cal. yaw'].values,  # Yaw angles
            df['cal. pitch'].values,  # Pitch angles
            df['cal. roll'].values  # Roll angles
        ])
        
        # Return all processed data for this user-video pair
        return {
            'orientation_array': orientation_array,  # (num_frames, 3) array of angles
            'tile_data': tile_data,  # List of tile overlap data
            'speed': speed,  # Head movement speed array
            'profile': profile  # User profile for Federated Learning
        }
    
    def process_all_data(self):
        """
        Main processing function that processes all videos and users.
        
        Paper: "We modified the dataset by separating it for each user and video category.
        This modification helped us test UVPFL approach and get high accuracy for each 
        video and video category separately."
        
        This function:
        1. Processes all 10 videos
        2. For each video, processes all 50 users
        3. Organizes data by category and user
        4. Creates user profiles for Federated Learning
        5. Saves all processed data in organized structure
        
        Returns:
            Dictionary of all user profiles organized by category
        """
        # Print header for preprocessing output
        print("=" * 60)
        print("UVPFL Data Preprocessing")
        print("=" * 60)
        
        # Dictionary to store all user profiles, organized by category
        # Structure: {category: [profile1, profile2, ...]}
        all_profiles = {cat: [] for cat in VIDEO_CATEGORIES.keys()}
        
        # Dictionary to store video metadata (fps, frame count, etc.)
        video_metadata = {}
        
        # Process each video (10 videos total)
        for video_name in tqdm(ALL_VIDEOS, desc="Processing videos"):
            # Print current video being processed
            print(f"\nProcessing: {video_name} ({VIDEO_NAME_MAPPING[video_name]})")
            
            # Get video metadata (frame count, fps, dimensions)
            metadata = self.get_video_metadata(video_name)
            if metadata is None:  # Skip if video file not found
                continue
            
            # Store metadata for this video
            video_metadata[video_name] = metadata
            
            # Save video metadata to JSON file
            with open(self.output_path / 'video_metadata' / f'{video_name}.json', 'w') as f:
                json.dump(metadata, f, indent=2)  # indent=2 for readable JSON
            
            # Update statistics
            self.stats['videos_processed'] += 1  # Increment video counter
            self.stats['total_frames'] += metadata['frame_count']  # Add frames to total
            
            # Get video category for organizing output
            category = VIDEO_TO_CATEGORY[video_name]  # e.g., 'ni_fast_paced'
            
            # Process each user for this video (50 users total)
            for user_id in tqdm(range(1, NUM_USERS + 1), desc=f"Users", leave=False):
                # Process this user-video pair (load data, calculate speed, create profile)
                result = self.process_user_video(video_name, user_id)
                if result is None:  # Skip if data not found
                    continue
                
                # Create directory for this user: processed_data/category/video/userXX/
                user_dir = self.output_path / category / video_name / f'user{user_id:02d}'
                user_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
                
                # Save orientation array (Y, PI, R angles) as NumPy file
                # Shape: (num_frames, 3) - used as target data for model training
                np.save(user_dir / 'orientation.npy', result['orientation_array'])
                
                # Save head movement speed array as NumPy file
                # Shape: (num_frames,) - used for user profiling
                np.save(user_dir / 'speed.npy', result['speed'])
                
                # Save tile data as JSON (if available)
                if result['tile_data']:  # Check if tile data exists
                    with open(user_dir / 'tiles.json', 'w') as f:
                        json.dump(result['tile_data'], f)  # Save tile overlap data
                
                # Save user profile as JSON (for Federated Learning and similarity matching)
                with open(user_dir / 'profile.json', 'w') as f:
                    json.dump(result['profile'], f, indent=2)  # Save profile with formatting
                
                # Add profile to category list (for later similarity matching)
                all_profiles[category].append(result['profile'])
                
                # Update statistics: add number of sequences for this user-video pair
                self.stats['total_sequences'] += result['profile']['num_sequences']
            
            # Update statistics: processed 50 users for this video
            self.stats['users_processed'] += NUM_USERS
            
            # Free memory after processing each video (important for large datasets)
            gc.collect()  # Garbage collection to free unused memory
        
        # ========================================================================
        # SAVE AGGREGATED DATA
        # ========================================================================
        
        # Save all user profiles organized by category
        # Paper: Used for Federated Learning and similar user matching
        for cat, profiles in all_profiles.items():  # Iterate through each category
            with open(self.output_path / 'user_profiles' / f'{cat}.json', 'w') as f:
                json.dump(profiles, f, indent=2)  # Save all profiles for this category
        
        # Save all video metadata in one file
        with open(self.output_path / 'video_metadata' / 'all.json', 'w') as f:
            json.dump(video_metadata, f, indent=2)  # Save metadata for all videos
        
        # Save configuration file (contains all constants and mappings)
        # This file is used by other scripts to understand the data structure
        config = {
            'video_categories': VIDEO_CATEGORIES,  # Category to videos mapping
            'video_to_category': VIDEO_TO_CATEGORY,  # Video to category mapping
            'video_name_mapping': VIDEO_NAME_MAPPING,  # Dataset name to paper name
            'all_videos': ALL_VIDEOS,  # List of all video names
            'num_users': NUM_USERS,  # Total number of users (50)
            'sequence_length': SEQUENCE_LENGTH,  # Frames per sequence (30)
            'frame_height': FRAME_HEIGHT,  # Frame height (120)
            'frame_width': FRAME_WIDTH  # Frame width (240)
        }
        with open(self.output_path / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)  # Save configuration
        
        # Save processing statistics
        with open(self.output_path / 'stats.json', 'w') as f:
            json.dump(self.stats, f, indent=2)  # Save statistics (total frames, sequences, etc.)
        
        # Print final summary
        print(f"\nDone! Videos: {self.stats['videos_processed']}, Sequences: {self.stats['total_sequences']}")
        
        return all_profiles  # Return all profiles for further use
    
    def create_train_test_split(self, test_ratio: float = 0.2, seed: int = 42):
        np.random.seed(seed)
        num_test = int(NUM_USERS * test_ratio)
        all_users = list(range(1, NUM_USERS + 1))
        np.random.shuffle(all_users)
        test_users = sorted(all_users[:num_test])
        train_users = sorted([u for u in range(1, NUM_USERS + 1) if u not in test_users])
        
        split = {'train_users': train_users, 'test_users': test_users, 'seed': seed}
        with open(self.output_path / 'train_test_split.json', 'w') as f:
            json.dump(split, f, indent=2)
        print(f"Train: {len(train_users)}, Test: {len(test_users)}")
        return split


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', default='360dataset')
    parser.add_argument('--output_path', default='processed_data')
    parser.add_argument('--test_ratio', type=float, default=0.2)
    args = parser.parse_args()
    
    preprocessor = UVPFLDataPreprocessor(args.dataset_path, args.output_path)
    preprocessor.process_all_data()
    preprocessor.create_train_test_split(args.test_ratio)


if __name__ == '__main__':
    main()

```

```python
"""
Data Preprocessing for UVPFL - Memory Efficient Version

This script preprocesses the 360-degree video dataset exactly as described in the paper:
1. Separates data for each user
2. Separates data for each video category (CG fast-paced, NI fast-paced, NI slow-paced)
3. Prepares head movement data (Yaw, Pitch, Roll) aligned with frames
4. Creates user profiles for Federated Learning

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- 30 frames per sequence
- Videos are ~60 seconds each at 30 fps = ~1800 frames
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV for video processing (reading video metadata)
import numpy as np  # Numerical computing library for arrays and math operations
import pandas as pd  # Data manipulation library for reading CSV files
from pathlib import Path  # Object-oriented filesystem paths (better than os.path)
from tqdm import tqdm  # Progress bar library for showing processing progress
import json  # JSON encoder/decoder for saving configuration and metadata
import gc  # Garbage collector for memory management (frees memory after processing each video)
from typing import Dict, List, Tuple, Optional  # Type hints for better code documentation

# ============================================================================
# VIDEO CATEGORY MAPPING (From Paper - Figure 7)
# ============================================================================
# Paper states: "We modified the dataset by separating it for each user and video category"
# These categories are used for user profiling in Federated Learning
VIDEO_CATEGORIES = {
    'cg_fast_paced': ['pacman', 'game', 'ride'],  # Computer-Generated fast-paced videos
    'ni_fast_paced': ['coaster', 'coaster2'],  # Natural-Image fast-paced videos
    'ni_slow_paced': ['diving', 'drive', 'landscape', 'panel', 'sport']  # Natural-Image slow-paced videos
}

# Create reverse mapping: video name -> category (for quick lookup)
VIDEO_TO_CATEGORY = {}  # Dictionary to map video name to its category
for category, videos in VIDEO_CATEGORIES.items():  # Iterate through each category
    for video in videos:  # For each video in the category
        VIDEO_TO_CATEGORY[video] = category  # Map video name to category

# Map dataset video names to paper's display names (for readability in output)
VIDEO_NAME_MAPPING = {
    'coaster': 'Roller Coaster',  # Dataset name -> Paper name
    'coaster2': 'Mega Coaster',
    'diving': 'Shark Shipwreck',
    'drive': 'Driving With',
    'game': 'Hog Rider',
    'landscape': 'Kangaroo Island',
    'pacman': 'Pac Man',
    'panel': 'Perils Penal',
    'ride': 'Chariot Race',
    'sport': 'SFR Sport'
}

# Get list of all 10 videos from the dataset
ALL_VIDEOS = list(VIDEO_TO_CATEGORY.keys())  # ['pacman', 'game', 'ride', 'coaster', 'coaster2', ...]

# ============================================================================
# DATASET CONSTANTS (From Paper)
# ============================================================================
NUM_USERS = 50  # Total number of users in the dataset (as per paper)
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification)
CHANNELS = 3  # RGB channels (3 color channels)


# ============================================================================
# UVPFL DATA PREPROCESSOR CLASS
# ============================================================================
class UVPFLDataPreprocessor:
    """
    Main preprocessor class that organizes data by user and video category.
    
    Paper requirement: "We modified the dataset by separating it for each user 
    and video category. This modification helped us test UVPFL approach and get 
    high accuracy for each video and video category separately."
    """
    
    def __init__(self, dataset_path: str, output_path: str):
        """
        Initialize the preprocessor with dataset and output paths.
        
        Args:
            dataset_path: Path to the 360dataset folder (contains content/ and sensory/)
            output_path: Path where processed data will be saved
        """
        self.dataset_path = Path(dataset_path)  # Convert to Path object for easier path operations
        self.output_path = Path(output_path)  # Output directory for processed data
        
        # Define paths to different data folders in the dataset
        self.saliency_path = self.dataset_path / 'content' / 'saliency'  # Saliency video files
        self.orientation_path = self.dataset_path / 'sensory' / 'orientation'  # Head movement CSV files
        self.tile_path = self.dataset_path / 'sensory' / 'tile'  # Tile overlap CSV files
        
        # Create the output directory structure (organized by category and user)
        self._create_output_directories()
        
        # Statistics dictionary to track processing progress
        self.stats = {
            'total_frames': 0,  # Total number of frames processed
            'total_sequences': 0,  # Total number of sequences created (frames - SEQUENCE_LENGTH)
            'users_processed': 0,  # Total number of user-video pairs processed
            'videos_processed': 0  # Number of videos processed
        }
    
    def _create_output_directories(self):
        """
        Create the output directory structure as per paper's methodology.
        
        Structure created:
        processed_data/
        ├── cg_fast_paced/
        │   ├── pacman/
        │   │   ├── user01/
        │   │   ├── user02/
        │   │   └── ...
        │   ├── game/
        │   └── ride/
        ├── ni_fast_paced/
        │   ├── coaster/
        │   └── coaster2/
        ├── ni_slow_paced/
        │   ├── diving/
        │   ├── drive/
        │   └── ...
        ├── user_profiles/  # User profiles for Federated Learning
        └── video_metadata/  # Video metadata (fps, frame count, etc.)
        """
        self.output_path.mkdir(parents=True, exist_ok=True)  # Create main output directory
        
        # Create directories for each video category (CG fast, NI fast, NI slow)
        for category in VIDEO_CATEGORIES.keys():  # Iterate through each category
            cat_path = self.output_path / category  # Path to category folder
            cat_path.mkdir(exist_ok=True)  # Create category directory if it doesn't exist
            
            # Create directories for each video within the category
            for video in VIDEO_CATEGORIES[category]:  # For each video in this category
                (cat_path / video).mkdir(exist_ok=True)  # Create video directory
        
        # Create directories for storing user profiles and video metadata
        (self.output_path / 'user_profiles').mkdir(exist_ok=True)  # For Federated Learning profiles
        (self.output_path / 'video_metadata').mkdir(exist_ok=True)  # For video information
        
        print(f"Created output directory structure at: {self.output_path}")
    
    def get_video_metadata(self, video_name: str) -> Dict:
        """
        Extract metadata from saliency video file.
        
        Paper: Videos are ~60 seconds each at 30 fps = ~1800 frames
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Dictionary with video metadata (frame count, fps, dimensions) or None if file not found
        """
        video_path = self.saliency_path / f'{video_name}_saliency.mp4'  # Path to saliency video file
        
        if not video_path.exists():  # Check if video file exists
            return None  # Return None if file not found
        
        cap = cv2.VideoCapture(str(video_path))  # Open video file using OpenCV
        if not cap.isOpened():  # Check if video opened successfully
            return None  # Return None if video couldn't be opened
        
        # Extract video metadata using OpenCV properties
        metadata = {
            'video_name': video_name,  # Video name (e.g., 'coaster')
            'category': VIDEO_TO_CATEGORY[video_name],  # Video category (e.g., 'ni_fast_paced')
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),  # Total number of frames (~1800)
            'fps': cap.get(cv2.CAP_PROP_FPS),  # Frames per second (typically 30)
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  # Video width in pixels
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),  # Video height in pixels
            'saliency_video_path': str(video_path)  # Full path to saliency video
        }
        
        cap.release()  # Release video capture object to free resources
        return metadata  # Return metadata dictionary
    
    def load_orientation_data(self, video_name: str, user_id: int) -> pd.DataFrame:
        """
        Load head movement orientation data for a specific user and video.
        
        Paper: "Yaw (Y), Pitch (PI), and Roll (R) angles are used to calculate 
        the user's current and predicted viewport"
        
        File format: {video_name}_user{user_id:02d}_orientation.csv
        Columns: no. frames, cal. yaw, cal. pitch, cal. roll (calibrated angles)
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            DataFrame with orientation data (Y, PI, R angles per frame) or None if file not found
        """
        # Construct path to orientation CSV file (e.g., 'coaster_user01_orientation.csv')
        file_path = self.orientation_path / f'{video_name}_user{user_id:02d}_orientation.csv'
        
        if not file_path.exists():  # Check if file exists
            return None  # Return None if file not found
        
        # Read CSV file into pandas DataFrame
        df = pd.read_csv(file_path, skipinitialspace=True)  # skipinitialspace removes leading spaces
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
        
        return df  # Return DataFrame with orientation data
    
    def load_tile_data(self, video_name: str, user_id: int) -> List[Dict]:
        """
        Load tile overlap data for a specific user and video.
        
        Paper: "Each frame is further divided into an l×k grid of tiles"
        Tile data shows which tiles overlap with user's Field of View (FoV)
        
        File format: {video_name}_user{user_id:02d}_tile.csv
        Format: frame_number, tile1, tile2, tile3, ... (comma-separated tile IDs)
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            List of dictionaries with frame number and tile IDs, or None if file not found
        """
        # Construct path to tile CSV file (e.g., 'coaster_user01_tile.csv')
        file_path = self.tile_path / f'{video_name}_user{user_id:02d}_tile.csv'
        
        if not file_path.exists():  # Check if file exists
            return None  # Return None if file not found
        
        tiles_data = []  # List to store tile data for each frame
        
        with open(file_path, 'r') as f:  # Open file for reading
            f.readline()  # Skip header line (first line)
            
            for line in f:  # Read each line (each line = one frame)
                parts = line.strip().split(',')  # Split line by comma
                frame_no = int(parts[0].strip())  # First element is frame number
                # Remaining elements are tile numbers (convert to integers, skip empty strings)
                tile_numbers = [int(t.strip()) for t in parts[1:] if t.strip()]
                
                # Store frame number and associated tile IDs
                tiles_data.append({'frame': frame_no, 'tiles': tile_numbers})
        
        return tiles_data  # Return list of tile data dictionaries
    
    def calculate_head_movement_speed(self, df: pd.DataFrame) -> np.ndarray:
        """
        Calculate head movement speed from orientation data.
        
        Paper: "Calculate head movement speed of User" (Algorithm 1, Phase 2)
        
        Speed is calculated as the magnitude of angular velocity:
        speed = sqrt(Δyaw² + Δpitch² + Δroll²)
        This represents how fast the user's head is moving in 3D space.
        
        Args:
            df: DataFrame with orientation data (columns: 'cal. yaw', 'cal. pitch', 'cal. roll')
            
        Returns:
            NumPy array of head movement speeds (one value per frame)
        """
        # Extract Yaw (Y), Pitch (PI), and Roll (R) angles as NumPy arrays
        yaw = df['cal. yaw'].values  # Horizontal rotation angles (degrees)
        pitch = df['cal. pitch'].values  # Vertical rotation angles (degrees)
        roll = df['cal. roll'].values  # Tilt angles (degrees)
        
        # Calculate angular velocity (change in angles between consecutive frames)
        # np.diff calculates difference: [a, b, c] -> [b-a, c-b]
        # prepend adds first value at beginning so arrays have same length
        d_yaw = np.diff(yaw, prepend=yaw[0])  # Change in yaw per frame
        d_pitch = np.diff(pitch, prepend=pitch[0])  # Change in pitch per frame
        d_roll = np.diff(roll, prepend=roll[0])  # Change in roll per frame
        
        # Calculate speed as magnitude of 3D angular velocity vector
        # This gives us how fast the head is moving overall
        return np.sqrt(d_yaw**2 + d_pitch**2 + d_roll**2)  # Euclidean distance in 3D angle space
    
    def process_user_video(self, video_name: str, user_id: int) -> Dict:
        """
        Process data for a single user-video pair.
        
        This is the core processing function that:
        1. Loads orientation data (Y, PI, R)
        2. Loads tile data
        3. Calculates head movement speed
        4. Creates user profile for Federated Learning
        
        Paper: "UVPFL profiles users based on their head movements for different 
        categories of videos"
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            user_id: User ID (1-50)
            
        Returns:
            Dictionary containing:
            - orientation_array: NumPy array of (Y, PI, R) angles per frame
            - tile_data: List of tile overlap data
            - speed: Head movement speed array
            - profile: User profile dictionary for similarity matching
        """
        # Load orientation data (head movement angles) for this user-video pair
        df = self.load_orientation_data(video_name, user_id)
        if df is None:  # If file not found, skip this user-video pair
            return None
        
        # Load tile data (which tiles overlap with user's viewport)
        tile_data = self.load_tile_data(video_name, user_id)
        
        # Calculate head movement speed (used in user profiling)
        speed = self.calculate_head_movement_speed(df)
        
        # Get video category (for organizing data and user profiling)
        category = VIDEO_TO_CATEGORY[video_name]  # e.g., 'ni_fast_paced'
        
        # Get number of frames in this video for this user
        num_frames = len(df)  # Typically ~1800 frames (60 seconds * 30 fps)
        
        # Create user profile for Federated Learning and similarity matching
        # Paper: "UVPFL profiles users based on their head movements for different 
        # categories of videos"
        profile = {
            'user_id': user_id,  # User identifier (1-50)
            'video_name': video_name,  # Video name (e.g., 'coaster')
            'category': category,  # Video category (e.g., 'ni_fast_paced')
            'num_frames': num_frames,  # Total frames for this user-video pair
            # Number of sequences that can be created (sliding window of 30 frames)
            'num_sequences': max(0, num_frames - SEQUENCE_LENGTH),
            # Statistical features for similarity matching (mean and std of each angle)
            'mean_yaw': float(df['cal. yaw'].mean()),  # Average yaw angle
            'std_yaw': float(df['cal. yaw'].std()),  # Standard deviation of yaw
            'mean_pitch': float(df['cal. pitch'].mean()),  # Average pitch angle
            'std_pitch': float(df['cal. pitch'].std()),  # Standard deviation of pitch
            'mean_roll': float(df['cal. roll'].mean()),  # Average roll angle
            'std_roll': float(df['cal. roll'].std()),  # Standard deviation of roll
            'mean_speed': float(speed.mean()),  # Average head movement speed
            'std_speed': float(speed.std())  # Standard deviation of speed
        }
        
        # Create NumPy array of orientation angles (Y, PI, R) for each frame
        # Shape: (num_frames, 3) where columns are [yaw, pitch, roll]
        # This will be used as target data for model training
        orientation_array = np.column_stack([
            df['cal. yaw'].values,  # Yaw angles
            df['cal. pitch'].values,  # Pitch angles
            df['cal. roll'].values  # Roll angles
        ])
        
        # Return all processed data for this user-video pair
        return {
            'orientation_array': orientation_array,  # (num_frames, 3) array of angles
            'tile_data': tile_data,  # List of tile overlap data
            'speed': speed,  # Head movement speed array
            'profile': profile  # User profile for Federated Learning
        }
    
    def process_all_data(self):
        """
        Main processing function that processes all videos and users.
        
        Paper: "We modified the dataset by separating it for each user and video category.
        This modification helped us test UVPFL approach and get high accuracy for each 
        video and video category separately."
        
        This function:
        1. Processes all 10 videos
        2. For each video, processes all 50 users
        3. Organizes data by category and user
        4. Creates user profiles for Federated Learning
        5. Saves all processed data in organized structure
        
        Returns:
            Dictionary of all user profiles organized by category
        """
        # Print header for preprocessing output
        print("=" * 60)
        print("UVPFL Data Preprocessing")
        print("=" * 60)
        
        # Dictionary to store all user profiles, organized by category
        # Structure: {category: [profile1, profile2, ...]}
        all_profiles = {cat: [] for cat in VIDEO_CATEGORIES.keys()}
        
        # Dictionary to store video metadata (fps, frame count, etc.)
        video_metadata = {}
        
        # Process each video (10 videos total)
        for video_name in tqdm(ALL_VIDEOS, desc="Processing videos"):
            # Print current video being processed
            print(f"\nProcessing: {video_name} ({VIDEO_NAME_MAPPING[video_name]})")
            
            # Get video metadata (frame count, fps, dimensions)
            metadata = self.get_video_metadata(video_name)
            if metadata is None:  # Skip if video file not found
                continue
            
            # Store metadata for this video
            video_metadata[video_name] = metadata
            
            # Save video metadata to JSON file
            with open(self.output_path / 'video_metadata' / f'{video_name}.json', 'w') as f:
                json.dump(metadata, f, indent=2)  # indent=2 for readable JSON
            
            # Update statistics
            self.stats['videos_processed'] += 1  # Increment video counter
            self.stats['total_frames'] += metadata['frame_count']  # Add frames to total
            
            # Get video category for organizing output
            category = VIDEO_TO_CATEGORY[video_name]  # e.g., 'ni_fast_paced'
            
            # Process each user for this video (50 users total)
            for user_id in tqdm(range(1, NUM_USERS + 1), desc=f"Users", leave=False):
                # Process this user-video pair (load data, calculate speed, create profile)
                result = self.process_user_video(video_name, user_id)
                if result is None:  # Skip if data not found
                    continue
                
                # Create directory for this user: processed_data/category/video/userXX/
                user_dir = self.output_path / category / video_name / f'user{user_id:02d}'
                user_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
                
                # Save orientation array (Y, PI, R angles) as NumPy file
                # Shape: (num_frames, 3) - used as target data for model training
                np.save(user_dir / 'orientation.npy', result['orientation_array'])
                
                # Save head movement speed array as NumPy file
                # Shape: (num_frames,) - used for user profiling
                np.save(user_dir / 'speed.npy', result['speed'])
                
                # Save tile data as JSON (if available)
                if result['tile_data']:  # Check if tile data exists
                    with open(user_dir / 'tiles.json', 'w') as f:
                        json.dump(result['tile_data'], f)  # Save tile overlap data
                
                # Save user profile as JSON (for Federated Learning and similarity matching)
                with open(user_dir / 'profile.json', 'w') as f:
                    json.dump(result['profile'], f, indent=2)  # Save profile with formatting
                
                # Add profile to category list (for later similarity matching)
                all_profiles[category].append(result['profile'])
                
                # Update statistics: add number of sequences for this user-video pair
                self.stats['total_sequences'] += result['profile']['num_sequences']
            
            # Update statistics: processed 50 users for this video
            self.stats['users_processed'] += NUM_USERS
            
            # Free memory after processing each video (important for large datasets)
            gc.collect()  # Garbage collection to free unused memory
        
        # ========================================================================
        # SAVE AGGREGATED DATA
        # ========================================================================
        
        # Save all user profiles organized by category
        # Paper: Used for Federated Learning and similar user matching
        for cat, profiles in all_profiles.items():  # Iterate through each category
            with open(self.output_path / 'user_profiles' / f'{cat}.json', 'w') as f:
                json.dump(profiles, f, indent=2)  # Save all profiles for this category
        
        # Save all video metadata in one file
        with open(self.output_path / 'video_metadata' / 'all.json', 'w') as f:
            json.dump(video_metadata, f, indent=2)  # Save metadata for all videos
        
        # Save configuration file (contains all constants and mappings)
        # This file is used by other scripts to understand the data structure
        config = {
            'video_categories': VIDEO_CATEGORIES,  # Category to videos mapping
            'video_to_category': VIDEO_TO_CATEGORY,  # Video to category mapping
            'video_name_mapping': VIDEO_NAME_MAPPING,  # Dataset name to paper name
            'all_videos': ALL_VIDEOS,  # List of all video names
            'num_users': NUM_USERS,  # Total number of users (50)
            'sequence_length': SEQUENCE_LENGTH,  # Frames per sequence (30)
            'frame_height': FRAME_HEIGHT,  # Frame height (120)
            'frame_width': FRAME_WIDTH  # Frame width (240)
        }
        with open(self.output_path / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)  # Save configuration
        
        # Save processing statistics
        with open(self.output_path / 'stats.json', 'w') as f:
            json.dump(self.stats, f, indent=2)  # Save statistics (total frames, sequences, etc.)
        
        # Print final summary
        print(f"\nDone! Videos: {self.stats['videos_processed']}, Sequences: {self.stats['total_sequences']}")
        
        return all_profiles  # Return all profiles for further use
    
    def create_train_test_split(self, test_ratio: float = 0.2, seed: int = 42):
        """
        Create train/test split by separating users.
        
        Paper: "We have two categories of users: trained users and users under testing.
        A trained user is a user who has already watched a video using UVPFL.
        A test user is a person who is currently watching the video."
        
        This function randomly splits 50 users into:
        - Train users: Used for training the model (80% = 40 users)
        - Test users: Used for testing/evaluation (20% = 10 users)
        
        Args:
            test_ratio: Ratio of users to use for testing (default: 0.2 = 20%)
            seed: Random seed for reproducibility (default: 42)
            
        Returns:
            Dictionary with train_users and test_users lists
        """
        # Set random seed for reproducibility (same seed = same split every time)
        np.random.seed(seed)
        
        # Calculate number of test users (20% of 50 = 10 users)
        num_test = int(NUM_USERS * test_ratio)
        
        # Create list of all user IDs (1 to 50)
        all_users = list(range(1, NUM_USERS + 1))
        
        # Shuffle users randomly
        np.random.shuffle(all_users)
        
        # Select first num_test users as test users (sorted for readability)
        test_users = sorted(all_users[:num_test])  # e.g., [2, 5, 8, 12, ...]
        
        # Remaining users are train users (sorted for readability)
        train_users = sorted([u for u in range(1, NUM_USERS + 1) if u not in test_users])
        
        # Create split dictionary
        split = {
            'train_users': train_users,  # List of user IDs for training (40 users)
            'test_users': test_users,  # List of user IDs for testing (10 users)
            'seed': seed  # Random seed used (for reproducibility)
        }
        
        # Save train/test split to JSON file
        with open(self.output_path / 'train_test_split.json', 'w') as f:
            json.dump(split, f, indent=2)  # Save split information
        
        # Print split summary
        print(f"Train: {len(train_users)}, Test: {len(test_users)}")
        
        return split  # Return split dictionary


# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================
def main():
    """
    Main function to run data preprocessing from command line.
    
    Usage:
        python data_preprocessing.py
        python data_preprocessing.py --dataset_path custom_path --output_path custom_output
        python data_preprocessing.py --test_ratio 0.3  # 30% test users
    """
    import argparse  # Command-line argument parsing
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='UVPFL Data Preprocessing')
    
    # Add command-line arguments
    parser.add_argument('--dataset_path', default='360dataset',
                        help='Path to the 360dataset folder')
    parser.add_argument('--output_path', default='processed_data',
                        help='Path to save processed data')
    parser.add_argument('--test_ratio', type=float, default=0.2,
                        help='Ratio of users for testing (default: 0.2 = 20%%)')
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Create preprocessor instance with specified paths
    preprocessor = UVPFLDataPreprocessor(args.dataset_path, args.output_path)
    
    # Process all data (all videos, all users)
    preprocessor.process_all_data()
    
    # Create train/test split (separate users into train and test sets)
    preprocessor.create_train_test_split(args.test_ratio)


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    # Run main function when script is executed directly (not imported)
    main()

```


Checking for linting errors:



The lint warning is about `tqdm` not being resolved; it's in `requirements.txt` and not a real error. Summary of `data_preprocessing.py`:

## **End-to-End Explanation of `data_preprocessing.py`**

### **Purpose**
Preprocesses the 360° video dataset per the paper: "We modified the dataset by separating it for each user and video category."

### **What It Does (Step-by-Step)**

1. **Setup & Configuration (Lines 16-51)**
   - Imports libraries (OpenCV, NumPy, Pandas, etc.)
   - Defines video categories (CG fast, NI fast, NI slow)
   - Maps videos to categories
   - Sets constants (50 users, 30 frames/sequence, 120×240 frame size)

2. **UVPFLDataPreprocessor Class (Lines 54-220)**
   - Main class that handles preprocessing

3. **Directory Structure Creation (Lines 64-73)**
   - Creates: `processed_data/category/video/userXX/`
   - Organizes data by category and user

4. **Video Metadata Extraction (Lines 75-91)**
   - Reads saliency video files
   - Extracts: frame count, fps, dimensions
   - Saves metadata for later use

5. **Data Loading Functions (Lines 93-113)**
   - `load_orientation_data()`: Loads Y, PI, R angles from CSV
   - `load_tile_data()`: Loads tile overlap data

6. **Head Movement Speed Calculation (Lines 115-118)**
   - Calculates speed as: `sqrt(Δyaw² + Δpitch² + Δroll²)`
   - Used for user profiling

7. **User-Video Processing (Lines 120-139)**
   - Processes each user-video pair
   - Creates user profile (mean/std of angles, speed)
   - Returns orientation array, tile data, speed, profile

8. **Main Processing Loop (Lines 141-206)**
   - Processes all 10 videos
   - For each video, processes all 50 users
   - Saves data organized by category/user
   - Creates user profiles for Federated Learning

9. **Train/Test Split (Lines 208-220)**
   - Splits 50 users into train (40) and test (10)
   - Saves split information

### **Output Structure Created**

```
processed_data/
├── cg_fast_paced/
│   ├── pacman/
│   │   ├── user01/
│   │   │   ├── orientation.npy  # (num_frames, 3) array of Y, PI, R
│   │   │   ├── speed.npy        # Head movement speed per frame
│   │   │   ├── tiles.json       # Tile overlap data
│   │   │   └── profile.json     # User profile for FL
│   │   ├── user02/
│   │   └── ...
│   ├── game/
│   └── ride/
├── ni_fast_paced/
│   ├── coaster/
│   └── coaster2/
├── ni_slow_paced/
│   └── ...
├── user_profiles/
│   ├── cg_fast_paced.json       # All profiles for this category
│   ├── ni_fast_paced.json
│   └── ni_slow_paced.json
├── video_metadata/
│   ├── coaster.json             # Metadata for each video
│   └── all.json                  # All video metadata
├── config.json                   # Configuration constants
├── stats.json                    # Processing statistics
└── train_test_split.json         # Train/test user split
```

### **Key Features**

1. Memory efficient: processes one video at a time, uses garbage collection
2. Organized by category: matches paper's requirement
3. User profiles: creates profiles for Federated Learning
4. Complete data: saves orientation, speed, tiles, profiles

### **How to Use**

```bash
# Basic usage
python data_preprocessing.py

# Custom paths
python data_preprocessing.py --dataset_path /path/to/360dataset --output_path /path/to/output

# Custom test ratio
python data_preprocessing.py --test_ratio 0.3  # 30% test users
```

The file is now commented line-by-line. Each line explains its purpose in the preprocessing pipeline.

```plaintext
processed_data/
├── cg_fast_paced/
│   ├── pacman/
│   │   ├── user01/
│   │   │   ├── orientation.npy  # (num_frames, 3) array of Y, PI, R
│   │   │   ├── speed.npy        # Head movement speed per frame
│   │   │   ├── tiles.json       # Tile overlap data
│   │   │   └── profile.json     # User profile for FL
│   │   ├── user02/
│   │   └── ...
│   ├── game/
│   └── ride/
├── ni_fast_paced/
│   ├── coaster/
│   └── coaster2/
├── ni_slow_paced/
│   └── ...
├── user_profiles/
│   ├── cg_fast_paced.json       # All profiles for this category
│   ├── ni_fast_paced.json
│   └── ni_slow_paced.json
├── video_metadata/
│   ├── coaster.json             # Metadata for each video
│   └── all.json                  # All video metadata
├── config.json                   # Configuration constants
├── stats.json                    # Processing statistics
└── train_test_split.json         # Train/test user split
```

```shellscript
# Basic usage
python data_preprocessing.py

# Custom paths
python data_preprocessing.py --dataset_path /path/to/360dataset --output_path /path/to/output

# Custom test ratio
python data_preprocessing.py --test_ratio 0.3  # 30% test users
```

---

**User**

explain it in more easy language with all the formulas used and also with a simple example 

---

**Cursor**


Creating a simple explanation with formulas and examples:


```markdown
# Data Preprocessing Explained - Simple Guide

## 🎯 What Does This Script Do? (In Simple Words)

Imagine you have a **360-degree video dataset** with:
- **10 videos** (like Roller Coaster, Pac Man, etc.)
- **50 users** who watched these videos
- For each user watching each video, we have:
  - **Head movement data** (where they looked - Yaw, Pitch, Roll angles)
  - **Tile data** (which parts of the video they saw)

**This script organizes all this messy data into a clean structure** so the AI model can learn from it!

---

## 📊 The Big Picture

```
Raw Dataset (Messy)
    ↓
[This Script]
    ↓
Organized Data (Clean)
    ↓
Ready for AI Training!
```

---

## 🔢 Formulas Used

### **Formula 1: Head Movement Speed**

**What it calculates:** How fast the user's head is moving (in degrees per frame)

**Formula:**
```
speed = √(Δyaw² + Δpitch² + Δroll²)
```

**In words:**
- Take the change in each angle (yaw, pitch, roll) between consecutive frames
- Square each change
- Add them together
- Take the square root

**Why?** This tells us if the user is moving their head quickly or slowly, which helps identify similar users.

**Example:**
```
Frame 1: yaw=10°, pitch=5°, roll=0°
Frame 2: yaw=12°, pitch=7°, roll=1°

Δyaw = 12 - 10 = 2°
Δpitch = 7 - 5 = 2°
Δroll = 1 - 0 = 1°

speed = √(2² + 2² + 1²)
      = √(4 + 4 + 1)
      = √9
      = 3° per frame
```

---

### **Formula 2: Number of Sequences**

**What it calculates:** How many training sequences we can create from a video

**Formula:**
```
num_sequences = max(0, num_frames - SEQUENCE_LENGTH)
```

**In words:**
- If you have 100 frames and need 30 frames per sequence
- You can create sequences starting at frame 1, 2, 3, ..., 71
- That's 100 - 30 = 70 sequences

**Example:**
```
Video has 1800 frames
Sequence length = 30 frames

Sequences:
- Sequence 1: frames 1-30 → predict frame 31
- Sequence 2: frames 2-31 → predict frame 32
- Sequence 3: frames 3-32 → predict frame 33
...
- Sequence 1770: frames 1770-1799 → predict frame 1800

Total sequences = 1800 - 30 = 1770
```

---

### **Formula 3: User Profile Statistics**

**What it calculates:** Statistical features of a user's head movement (for finding similar users)

**Formulas:**
```
mean_yaw = average of all yaw angles
std_yaw = standard deviation of yaw angles
mean_pitch = average of all pitch angles
std_pitch = standard deviation of pitch angles
mean_roll = average of all roll angles
std_roll = standard deviation of roll angles
mean_speed = average of all speeds
std_speed = standard deviation of speeds
```

**In words:**
- **Mean (average):** Where does the user typically look?
- **Standard deviation:** How much does the user move around?

**Example:**
```
User watching "Roller Coaster":
Yaw angles: [10°, 12°, 15°, 8°, 11°, ...] (1800 values)

mean_yaw = (10 + 12 + 15 + 8 + 11 + ...) / 1800
         = 10.5°  (user typically looks 10.5° to the right)

std_yaw = √(average of (each_angle - mean_yaw)²)
        = 5.2°  (user moves around ±5.2° on average)
```

**Why?** Users with similar means and stds have similar viewing patterns!

---

## 📁 Step-by-Step: What Happens to the Data

### **Step 1: Read Raw Data**

**Input:**
```
360dataset/
├── sensory/orientation/
│   ├── coaster_user01_orientation.csv  ← Head movement data
│   ├── coaster_user02_orientation.csv
│   └── ...
└── sensory/tile/
    ├── coaster_user01_tile.csv  ← Tile overlap data
    └── ...
```

**What's in orientation CSV?**
```
no. frames, cal. yaw, cal. pitch, cal. roll
00001, 10.5, 5.2, 0.1
00002, 11.2, 5.8, 0.2
00003, 12.1, 6.1, 0.1
...
```

**What's in tile CSV?**
```
no. frames, tile numbers
00001, 45, 46, 47, 65, 66, 67
00002, 46, 47, 48, 66, 67, 68
...
```

---

### **Step 2: Process Each User-Video Pair**

**For User 1 watching "Roller Coaster":**

1. **Load orientation data:**
   ```python
   # Read CSV file
   yaw = [10.5, 11.2, 12.1, ...]  # 1800 values
   pitch = [5.2, 5.8, 6.1, ...]   # 1800 values
   roll = [0.1, 0.2, 0.1, ...]    # 1800 values
   ```

2. **Calculate speed:**
   ```python
   # Frame 1 to Frame 2:
   Δyaw = 11.2 - 10.5 = 0.7°
   Δpitch = 5.8 - 5.2 = 0.6°
   Δroll = 0.2 - 0.1 = 0.1°
   
   speed_frame1 = √(0.7² + 0.6² + 0.1²) = √(0.49 + 0.36 + 0.01) = √0.86 = 0.93°
   
   # Repeat for all frames → speed = [0.93, 1.2, 0.8, ...] (1800 values)
   ```

3. **Create user profile:**
   ```python
   profile = {
       'mean_yaw': 10.5°,      # Average yaw angle
       'std_yaw': 5.2°,        # How much yaw varies
       'mean_pitch': 5.8°,     # Average pitch angle
       'std_pitch': 3.1°,      # How much pitch varies
       'mean_speed': 1.5°,     # Average head movement speed
       ...
   }
   ```

4. **Create orientation array:**
   ```python
   # Combine all angles into one array
   orientation_array = [
       [10.5, 5.2, 0.1],  # Frame 1: [yaw, pitch, roll]
       [11.2, 5.8, 0.2],  # Frame 2: [yaw, pitch, roll]
       [12.1, 6.1, 0.1],  # Frame 3: [yaw, pitch, roll]
       ...
   ]
   # Shape: (1800, 3) - 1800 frames, 3 angles each
   ```

---

### **Step 3: Organize by Category**

**The script organizes data like this:**

```
processed_data/
├── ni_fast_paced/          ← Category: Natural Image Fast
│   ├── coaster/            ← Video: Roller Coaster
│   │   ├── user01/         ← User 1's data
│   │   │   ├── orientation.npy  ← (1800, 3) array
│   │   │   ├── speed.npy          ← (1800,) array
│   │   │   ├── tiles.json         ← Tile overlap data
│   │   │   └── profile.json       ← User profile
│   │   ├── user02/
│   │   └── ... (50 users)
│   └── coaster2/
├── cg_fast_paced/          ← Category: Computer Generated Fast
│   ├── pacman/
│   ├── game/
│   └── ride/
└── ni_slow_paced/          ← Category: Natural Image Slow
    └── ...
```

**Why organize by category?**
- Paper says: "UVPFL profiles users based on their head movements for different categories of videos"
- Users watching fast-paced videos behave differently than slow-paced videos
- We need to find similar users **within the same category**

---

### **Step 4: Create Train/Test Split**

**The script splits 50 users:**

```
All Users: [1, 2, 3, 4, ..., 50]

Random Shuffle: [23, 5, 41, 12, ..., 8]

Train Users (80% = 40 users): [1, 2, 3, 5, 7, ..., 48]
Test Users (20% = 10 users): [12, 15, 23, 28, ..., 50]
```

**Why?**
- **Train users:** Used to train the AI model
- **Test users:** Used to test if the model works (like a final exam)

---

## 🎬 Complete Example: Processing One User-Video Pair

Let's trace through **User 5 watching "Pac Man"** (CG fast-paced video):

### **Input Files:**
1. `pacman_user05_orientation.csv` (head movement data)
2. `pacman_user05_tile.csv` (tile overlap data)

### **Step 1: Load Orientation Data**

```python
# Read CSV file
CSV Content:
frame, cal. yaw, cal. pitch, cal. roll
00001, 15.2, -5.3, 0.5
00002, 16.1, -4.8, 0.6
00003, 17.5, -4.2, 0.4
...
(1800 rows total)

# Convert to arrays:
yaw = [15.2, 16.1, 17.5, ...]     # 1800 values
pitch = [-5.3, -4.8, -4.2, ...]   # 1800 values
roll = [0.5, 0.6, 0.4, ...]       # 1800 values
```

### **Step 2: Calculate Head Movement Speed**

```python
# Calculate speed for each frame transition:

# Frame 1 → Frame 2:
Δyaw = 16.1 - 15.2 = 0.9°
Δpitch = -4.8 - (-5.3) = 0.5°
Δroll = 0.6 - 0.5 = 0.1°

speed[1] = √(0.9² + 0.5² + 0.1²)
         = √(0.81 + 0.25 + 0.01)
         = √1.07
         = 1.03° per frame

# Frame 2 → Frame 3:
Δyaw = 17.5 - 16.1 = 1.4°
Δpitch = -4.2 - (-4.8) = 0.6°
Δroll = 0.4 - 0.6 = -0.2°

speed[2] = √(1.4² + 0.6² + (-0.2)²)
         = √(1.96 + 0.36 + 0.04)
         = √2.36
         = 1.54° per frame

# Continue for all frames...
# Result: speed = [1.03, 1.54, 0.92, ...] (1800 values)
```

### **Step 3: Calculate Statistics (User Profile)**

```python
# Calculate mean (average):
mean_yaw = (15.2 + 16.1 + 17.5 + ...) / 1800
         = 18.5°  # User typically looks 18.5° to the right

mean_pitch = (-5.3 + -4.8 + -4.2 + ...) / 1800
           = -4.2°  # User typically looks 4.2° down

mean_speed = (1.03 + 1.54 + 0.92 + ...) / 1800
           = 2.1° per frame  # User moves head at 2.1° per frame on average

# Calculate standard deviation (how much variation):
std_yaw = √(average of (each_yaw - 18.5)²)
        = 8.3°  # User's yaw varies by ±8.3° on average

std_speed = √(average of (each_speed - 2.1)²)
          = 1.2°  # Speed varies by ±1.2° per frame
```

### **Step 4: Create Orientation Array**

```python
# Combine all angles into one NumPy array:
orientation_array = np.array([
    [15.2, -5.3, 0.5],   # Frame 1: [yaw, pitch, roll]
    [16.1, -4.8, 0.6],   # Frame 2: [yaw, pitch, roll]
    [17.5, -4.2, 0.4],   # Frame 3: [yaw, pitch, roll]
    ...
])

# Shape: (1800, 3)
# This will be used as TARGET data for model training
# Model learns: Given 30 frames → predict next frame's [yaw, pitch, roll]
```

### **Step 5: Save Everything**

```python
# Save to: processed_data/cg_fast_paced/pacman/user05/

# 1. Save orientation array (NumPy format - fast loading)
np.save('orientation.npy', orientation_array)
# File size: ~21 KB (1800 × 3 × 4 bytes per float)

# 2. Save speed array
np.save('speed.npy', speed)
# File size: ~7 KB (1800 × 4 bytes)

# 3. Save user profile (JSON format - human readable)
profile = {
    'user_id': 5,
    'video_name': 'pacman',
    'category': 'cg_fast_paced',
    'mean_yaw': 18.5,
    'std_yaw': 8.3,
    'mean_pitch': -4.2,
    'std_pitch': 3.1,
    'mean_speed': 2.1,
    'std_speed': 1.2,
    'num_frames': 1800,
    'num_sequences': 1770  # 1800 - 30 = 1770
}
json.dump(profile, 'profile.json')
```

---

## 🔍 Real-World Analogy

Think of it like organizing a **library**:

### **Before (Raw Dataset):**
- All books scattered everywhere
- No organization
- Hard to find what you need

### **After (Processed Data):**
- Books organized by **category** (Fiction, Non-fiction, etc.)
- Each category has **shelves** (videos)
- Each shelf has **books** (users)
- Each book has **chapters** (frames) with **page numbers** (orientation data)

**Just like:**
- Category = Video category (CG fast, NI fast, NI slow)
- Shelf = Video name (Pac Man, Roller Coaster, etc.)
- Book = User (user01, user02, ..., user50)
- Chapter = Frame (frame 1, frame 2, ..., frame 1800)
- Page numbers = Orientation data (yaw, pitch, roll angles)

---

## 📈 What Gets Created (Summary)

### **For Each User-Video Pair:**
1. **orientation.npy** - Array of (Y, PI, R) angles for each frame
2. **speed.npy** - Head movement speed for each frame
3. **tiles.json** - Which tiles user viewed (optional)
4. **profile.json** - User statistics (for finding similar users)

### **Aggregated Files:**
1. **user_profiles/{category}.json** - All user profiles for a category
2. **video_metadata/{video}.json** - Video information (fps, frame count)
3. **config.json** - All constants and mappings
4. **train_test_split.json** - Which users are for training/testing

---

## 🎯 Why This Organization Matters

### **For Federated Learning:**
- Each user's data is **separate** (privacy-preserving)
- We can train models **per user** or **per category**
- User profiles help find **similar users** (for cold-start problem)

### **For Model Training:**
- Easy to load data for specific users/categories
- Efficient data loading (NumPy arrays load fast)
- Clear train/test split

### **For Similar User Matching:**
- User profiles contain statistical features
- Can compare profiles to find similar viewing patterns
- Helps new users by matching with similar trained users

---

## 💡 Key Takeaways

1. **Input:** Messy CSV files with head movement data
2. **Process:** Calculate statistics, organize by category/user
3. **Output:** Clean, organized data ready for AI training
4. **Formulas:**
   - Speed = √(Δyaw² + Δpitch² + Δroll²)
   - Sequences = frames - 30
   - Statistics = mean and std of angles/speed
5. **Organization:** By category → video → user (matches paper requirement)

---

## 🚀 Next Steps

After preprocessing:
1. **Data Loader** (`data_loader.py`) loads this organized data
2. **Model** (`model.py`) trains on sequences of 30 frames
3. **Viewport Prediction** (`viewport_prediction.py`) uses user profiles to find similar users
4. **Training** (`train.py`) trains the AI model

**This preprocessing is the foundation for everything else!** 🎉

```


Created a guide: `DATA_PREPROCESSING_EXPLAINED.md`. Summary:

## **Simple explanation**

### **What it does (one sentence)**
Takes messy CSV files with head movement data and organizes them by user and video category so the AI can learn from them.

---

## **Formulas used**

### **1. Head movement speed**
```
speed = √(Δyaw² + Δpitch² + Δroll²)
```

**Example:**
- Frame 1: yaw=10°, pitch=5°, roll=0°
- Frame 2: yaw=12°, pitch=7°, roll=1°
- Speed = √((12-10)² + (7-5)² + (1-0)²) = √(4+4+1) = **3° per frame**

**Why:** Measures how fast the head moves, used to find similar users.

---

### **2. Number of sequences**
```
num_sequences = num_frames - 30
```

**Example:**
- Video has 1800 frames
- Need 30 frames per sequence
- Can create: 1800 - 30 = **1770 sequences**
- Sequence 1: frames 1-30 → predict frame 31
- Sequence 2: frames 2-31 → predict frame 32
- etc.

---

### **3. User statistics (mean & standard deviation)**
```
mean_yaw = average of all yaw angles
std_yaw = how much yaw varies
```

**Example:**
- User's yaw angles: [10°, 12°, 15°, 8°, 11°, ...]
- Mean = 10.5° (typically looks 10.5° right)
- Std = 5.2° (varies by ±5.2°)

**Why:** Users with similar means/stds have similar viewing patterns.

---

## **Complete example: User 5 watching "Pac Man"**

### **Step 1: Read data**
```
CSV file: pacman_user05_orientation.csv
Frame 1: yaw=15.2°, pitch=-5.3°, roll=0.5°
Frame 2: yaw=16.1°, pitch=-4.8°, roll=0.6°
Frame 3: yaw=17.5°, pitch=-4.2°, roll=0.4°
... (1800 frames total)
```

### **Step 2: Calculate speed**
```
Frame 1→2:
  Δyaw = 16.1 - 15.2 = 0.9°
  Δpitch = -4.8 - (-5.3) = 0.5°
  Δroll = 0.6 - 0.5 = 0.1°
  speed = √(0.9² + 0.5² + 0.1²) = 1.03° per frame
```

### **Step 3: Calculate statistics**
```
mean_yaw = 18.5°      (typically looks 18.5° right)
std_yaw = 8.3°        (varies by ±8.3°)
mean_speed = 2.1°     (moves at 2.1° per frame on average)
```

### **Step 4: Save organized data**
```
processed_data/
└── cg_fast_paced/        ← Category
    └── pacman/           ← Video
        └── user05/       ← User
            ├── orientation.npy  ← (1800, 3) array of angles
            ├── speed.npy         ← (1800,) array of speeds
            └── profile.json      ← User statistics
```

---

## **Real-world analogy**

**Before (raw data):**
- Books scattered everywhere
- Hard to find anything

**After (processed data):**
- Organized by category (Fiction, Non-fiction)
- Each category has shelves (videos)
- Each shelf has books (users)
- Each book has chapters (frames) with page numbers (angles)

---

## **Why this matters**

1. For Federated Learning: Each user's data stays separate (privacy)
2. For finding similar users: Profiles help match users with similar viewing patterns
3. For training: Clean, organized data loads faster and is easier to use

---

## **Output structure**

```
processed_data/
├── cg_fast_paced/pacman/user05/
│   ├── orientation.npy  ← (1800, 3) - angles for each frame
│   ├── speed.npy         ← (1800,) - speed for each frame
│   └── profile.json      ← Statistics for similarity matching
├── user_profiles/
│   └── cg_fast_paced.json  ← All profiles for this category
└── train_test_split.json   ← Which users are train/test
```

---

The detailed guide is in `DATA_PREPROCESSING_EXPLAINED.md` with:
- All formulas explained
- Step-by-step examples
- Real-world analogies
- Visual structure diagrams

The script is now commented line-by-line in `data_preprocessing.py` for easy understanding.

```plaintext
speed = √(Δyaw² + Δpitch² + Δroll²)
```

```plaintext
num_sequences = num_frames - 30
```

```plaintext
mean_yaw = average of all yaw angles
std_yaw = how much yaw varies
```

```plaintext
CSV file: pacman_user05_orientation.csv
Frame 1: yaw=15.2°, pitch=-5.3°, roll=0.5°
Frame 2: yaw=16.1°, pitch=-4.8°, roll=0.6°
Frame 3: yaw=17.5°, pitch=-4.2°, roll=0.4°
... (1800 frames total)
```

```plaintext
Frame 1→2:
  Δyaw = 16.1 - 15.2 = 0.9°
  Δpitch = -4.8 - (-5.3) = 0.5°
  Δroll = 0.6 - 0.5 = 0.1°
  speed = √(0.9² + 0.5² + 0.1²) = 1.03° per frame
```

```plaintext
mean_yaw = 18.5°      (typically looks 18.5° right)
std_yaw = 8.3°        (varies by ±8.3°)
mean_speed = 2.1°     (moves at 2.1° per frame on average)
```

```plaintext
processed_data/
└── cg_fast_paced/        ← Category
    └── pacman/           ← Video
        └── user05/       ← User
            ├── orientation.npy  ← (1800, 3) array of angles
            ├── speed.npy         ← (1800,) array of speeds
            └── profile.json      ← User statistics
```

```plaintext
processed_data/
├── cg_fast_paced/pacman/user05/
│   ├── orientation.npy  ← (1800, 3) - angles for each frame
│   ├── speed.npy         ← (1800,) - speed for each frame
│   └── profile.json      ← Statistics for similarity matching
├── user_profiles/
│   └── cg_fast_paced.json  ← All profiles for this category
└── train_test_split.json   ← Which users are train/test
```

---

**User**

addd comments without changing the code in data_loader.py and also explain it to me in easy language and in detail 

---

**Cursor**


Reading `data_loader.py` to add comments and prepare a simple explanation:



Adding detailed comments to `data_loader.py` and preparing a simple explanation:


```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface (for file operations)
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration files
import numpy as np  # Numerical computing library for array operations
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (better than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures
from tqdm import tqdm  # Progress bar library for showing loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)
```


Reading the file again to match the exact formatting:



Adding comments section by section:


```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand.
    Caches video capture objects for efficiency.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder
            target_size: (width, height) for resizing frames
        """
        self.saliency_path = Path(saliency_path)
        self.target_size = target_size
        self._video_captures = {}  # Cache for video capture objects
        self._video_frame_counts = {}
    
    def get_video_path(self, video_name: str) -> Path:
        """Get path to saliency video."""
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """Get total frame count for a video."""
        if video_name not in self._video_frame_counts:
            video_path = self.get_video_path(video_name)
            cap = cv2.VideoCapture(str(video_path))
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video.
        
        Args:
            video_name: Name of the video
            frame_idx: Frame index (0-based)
            
        Returns:
            Frame as numpy array (height, width, channels) normalized to [0, 1]
        """
        video_path = self.get_video_path(video_name)
        
        # Create new capture for each extraction (thread-safe)
        cap = cv2.VideoCapture(str(video_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            # Return black frame if extraction fails
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame
        frame = cv2.resize(frame, self.target_size)
        
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        frame = frame.astype(np.float32) / 255.0
        
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of frames from the video.
        
        Args:
            video_name: Name of the video
            start_frame: Starting frame index
            sequence_length: Number of frames to extract
            
        Returns:
            Sequence as numpy array (sequence_length, height, width, channels)
        """
        video_path = self.get_video_path(video_name)
        cap = cv2.VideoCapture(str(video_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frames = []
        for _ in range(sequence_length):
            ret, frame = cap.read()
            if not ret:
                # Pad with black frames if video ends
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize and convert
            frame = cv2.resize(frame, self.target_size)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.astype(np.float32) / 255.0
            frames.append(frame)
        
        cap.release()
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """Close all cached video captures."""
        for cap in self._video_captures.values():
            cap.release()
        self._video_captures.clear()


class UVPFLDataLoader:
    """
    Main data loader for UVPFL model.
    
    Provides:
    - Efficient data loading with on-demand frame extraction
    - Sequence creation for model input
    - Train/test split handling
    - Batch generation with prefetching
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence (default: 30)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second)
            batch_size: Batch size for training
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Load configuration
        self._load_config()
        
        # Load train/test split
        self._load_split()
        
        # Build sample index
        self._build_sample_index()
    
    def _load_config(self):
        """Load configuration from processed data."""
        config_path = self.processed_path / 'config.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.video_categories = self.config['video_categories']
        self.video_to_category = self.config['video_to_category']
        self.all_videos = self.config['all_videos']
        self.num_users = self.config['num_users']
    
    def _load_split(self):
        """Load train/test split."""
        split_path = self.processed_path / 'train_test_split.json'
        with open(split_path, 'r') as f:
            split = json.load(f)
        
        self.train_users = split['train_users']
        self.test_users = split['test_users']
    
    def _build_sample_index(self):
        """
        Build index of all available samples.
        Each sample is (video_name, user_id, start_frame, target_frame).
        """
        self.train_samples = []
        self.test_samples = []
        
        print("Building sample index...")
        
        for category, videos in self.video_categories.items():
            for video_name in videos:
                # Get frame count for this video
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Maximum start frame (need sequence_length + prediction_horizon frames)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count
                    orientation = np.load(orientation_path)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples (stride of 15 frames = 0.5 second to reduce redundancy)
                    stride = 15
                    for start_frame in range(0, actual_max_start, stride):
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        sample = {
                            'video_name': video_name,
                            'category': category,
                            'user_id': user_id,
                            'start_frame': start_frame,
                            'target_frame': target_frame
                        }
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """Load orientation data for a user-video pair."""
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single sample (frames sequence and target orientation).
        
        Args:
            sample: Sample dictionary with video_name, user_id, start_frame, target_frame
            
        Returns:
            Tuple of (frames_sequence, target_orientation)
            - frames_sequence: (sequence_length, height, width, channels)
            - target_orientation: (3,) = (yaw, pitch, roll)
        """
        video_name = sample['video_name']
        category = sample['category']
        user_id = sample['user_id']
        start_frame = sample['start_frame']
        target_frame = sample['target_frame']
        
        # Extract frame sequence
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation and get target
        orientation = self._load_orientation(video_name, category, user_id)
        target = orientation[target_frame]  # (yaw, pitch, roll)
        
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```

```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video.
        
        Args:
            video_name: Name of the video
            frame_idx: Frame index (0-based)
            
        Returns:
            Frame as numpy array (height, width, channels) normalized to [0, 1]
        """
        video_path = self.get_video_path(video_name)
        
        # Create new capture for each extraction (thread-safe)
        cap = cv2.VideoCapture(str(video_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            # Return black frame if extraction fails
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame
        frame = cv2.resize(frame, self.target_size)
        
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        frame = frame.astype(np.float32) / 255.0
        
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of frames from the video.
        
        Args:
            video_name: Name of the video
            start_frame: Starting frame index
            sequence_length: Number of frames to extract
            
        Returns:
            Sequence as numpy array (sequence_length, height, width, channels)
        """
        video_path = self.get_video_path(video_name)
        cap = cv2.VideoCapture(str(video_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frames = []
        for _ in range(sequence_length):
            ret, frame = cap.read()
            if not ret:
                # Pad with black frames if video ends
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize and convert
            frame = cv2.resize(frame, self.target_size)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.astype(np.float32) / 255.0
            frames.append(frame)
        
        cap.release()
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """Close all cached video captures."""
        for cap in self._video_captures.values():
            cap.release()
        self._video_captures.clear()


class UVPFLDataLoader:
    """
    Main data loader for UVPFL model.
    
    Provides:
    - Efficient data loading with on-demand frame extraction
    - Sequence creation for model input
    - Train/test split handling
    - Batch generation with prefetching
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence (default: 30)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second)
            batch_size: Batch size for training
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Load configuration
        self._load_config()
        
        # Load train/test split
        self._load_split()
        
        # Build sample index
        self._build_sample_index()
    
    def _load_config(self):
        """Load configuration from processed data."""
        config_path = self.processed_path / 'config.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.video_categories = self.config['video_categories']
        self.video_to_category = self.config['video_to_category']
        self.all_videos = self.config['all_videos']
        self.num_users = self.config['num_users']
    
    def _load_split(self):
        """Load train/test split."""
        split_path = self.processed_path / 'train_test_split.json'
        with open(split_path, 'r') as f:
            split = json.load(f)
        
        self.train_users = split['train_users']
        self.test_users = split['test_users']
    
    def _build_sample_index(self):
        """
        Build index of all available samples.
        Each sample is (video_name, user_id, start_frame, target_frame).
        """
        self.train_samples = []
        self.test_samples = []
        
        print("Building sample index...")
        
        for category, videos in self.video_categories.items():
            for video_name in videos:
                # Get frame count for this video
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Maximum start frame (need sequence_length + prediction_horizon frames)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count
                    orientation = np.load(orientation_path)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples (stride of 15 frames = 0.5 second to reduce redundancy)
                    stride = 15
                    for start_frame in range(0, actual_max_start, stride):
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        sample = {
                            'video_name': video_name,
                            'category': category,
                            'user_id': user_id,
                            'start_frame': start_frame,
                            'target_frame': target_frame
                        }
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """Load orientation data for a user-video pair."""
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single sample (frames sequence and target orientation).
        
        Args:
            sample: Sample dictionary with video_name, user_id, start_frame, target_frame
            
        Returns:
            Tuple of (frames_sequence, target_orientation)
            - frames_sequence: (sequence_length, height, width, channels)
            - target_orientation: (3,) = (yaw, pitch, roll)
        """
        video_name = sample['video_name']
        category = sample['category']
        user_id = sample['user_id']
        start_frame = sample['start_frame']
        target_frame = sample['target_frame']
        
        # Extract frame sequence
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation and get target
        orientation = self._load_orientation(video_name, category, user_id)
        target = orientation[target_frame]  # (yaw, pitch, roll)
        
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```

```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video at a specific index.
        
        Paper: Frames are extracted from saliency videos and resized to (120, 240, 3)
        for model input.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            frame_idx: Frame index (0-based, e.g., 0 = first frame, 1 = second frame)
            
        Returns:
            Frame as numpy array with shape (height, width, channels) = (120, 240, 3)
            Values normalized to [0, 1] range (for neural network training)
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        
        # Create new video capture object for each extraction (thread-safe approach)
        # This ensures each extraction is independent and doesn't interfere with others
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the desired frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Read the frame at that position
        # ret = True if frame was read successfully, False otherwise
        # frame = the actual frame image (BGR format)
        ret, frame = cap.read()
        # Release video capture to free resources
        cap.release()
        
        # If frame extraction failed (e.g., frame index out of bounds)
        if not ret:
            # Return a black frame (all zeros) with correct dimensions
            # Shape: (height, width, channels) = (120, 240, 3)
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame to target size (240 width, 120 height)
        # Paper: Input shape is (30, 120, 240, 3), so each frame must be 120×240
        frame = cv2.resize(frame, self.target_size)
        
        # Convert from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
        # OpenCV uses BGR by default, but neural networks expect RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Neural networks train better with normalized inputs
        # Formula: normalized = original / 255.0
        frame = frame.astype(np.float32) / 255.0
        
        # Return processed frame ready for model input
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of frames from the video.
        
        Args:
            video_name: Name of the video
            start_frame: Starting frame index
            sequence_length: Number of frames to extract
            
        Returns:
            Sequence as numpy array (sequence_length, height, width, channels)
        """
        video_path = self.get_video_path(video_name)
        cap = cv2.VideoCapture(str(video_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frames = []
        for _ in range(sequence_length):
            ret, frame = cap.read()
            if not ret:
                # Pad with black frames if video ends
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize and convert
            frame = cv2.resize(frame, self.target_size)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.astype(np.float32) / 255.0
            frames.append(frame)
        
        cap.release()
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """Close all cached video captures."""
        for cap in self._video_captures.values():
            cap.release()
        self._video_captures.clear()


class UVPFLDataLoader:
    """
    Main data loader for UVPFL model.
    
    Provides:
    - Efficient data loading with on-demand frame extraction
    - Sequence creation for model input
    - Train/test split handling
    - Batch generation with prefetching
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence (default: 30)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second)
            batch_size: Batch size for training
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Load configuration
        self._load_config()
        
        # Load train/test split
        self._load_split()
        
        # Build sample index
        self._build_sample_index()
    
    def _load_config(self):
        """Load configuration from processed data."""
        config_path = self.processed_path / 'config.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.video_categories = self.config['video_categories']
        self.video_to_category = self.config['video_to_category']
        self.all_videos = self.config['all_videos']
        self.num_users = self.config['num_users']
    
    def _load_split(self):
        """Load train/test split."""
        split_path = self.processed_path / 'train_test_split.json'
        with open(split_path, 'r') as f:
            split = json.load(f)
        
        self.train_users = split['train_users']
        self.test_users = split['test_users']
    
    def _build_sample_index(self):
        """
        Build index of all available samples.
        Each sample is (video_name, user_id, start_frame, target_frame).
        """
        self.train_samples = []
        self.test_samples = []
        
        print("Building sample index...")
        
        for category, videos in self.video_categories.items():
            for video_name in videos:
                # Get frame count for this video
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Maximum start frame (need sequence_length + prediction_horizon frames)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count
                    orientation = np.load(orientation_path)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples (stride of 15 frames = 0.5 second to reduce redundancy)
                    stride = 15
                    for start_frame in range(0, actual_max_start, stride):
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        sample = {
                            'video_name': video_name,
                            'category': category,
                            'user_id': user_id,
                            'start_frame': start_frame,
                            'target_frame': target_frame
                        }
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """Load orientation data for a user-video pair."""
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single sample (frames sequence and target orientation).
        
        Args:
            sample: Sample dictionary with video_name, user_id, start_frame, target_frame
            
        Returns:
            Tuple of (frames_sequence, target_orientation)
            - frames_sequence: (sequence_length, height, width, channels)
            - target_orientation: (3,) = (yaw, pitch, roll)
        """
        video_name = sample['video_name']
        category = sample['category']
        user_id = sample['user_id']
        start_frame = sample['start_frame']
        target_frame = sample['target_frame']
        
        # Extract frame sequence
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation and get target
        orientation = self._load_orientation(video_name, category, user_id)
        target = orientation[target_frame]  # (yaw, pitch, roll)
        
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```

```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video at a specific index.
        
        Paper: Frames are extracted from saliency videos and resized to (120, 240, 3)
        for model input.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            frame_idx: Frame index (0-based, e.g., 0 = first frame, 1 = second frame)
            
        Returns:
            Frame as numpy array with shape (height, width, channels) = (120, 240, 3)
            Values normalized to [0, 1] range (for neural network training)
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        
        # Create new video capture object for each extraction (thread-safe approach)
        # This ensures each extraction is independent and doesn't interfere with others
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the desired frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Read the frame at that position
        # ret = True if frame was read successfully, False otherwise
        # frame = the actual frame image (BGR format)
        ret, frame = cap.read()
        # Release video capture to free resources
        cap.release()
        
        # If frame extraction failed (e.g., frame index out of bounds)
        if not ret:
            # Return a black frame (all zeros) with correct dimensions
            # Shape: (height, width, channels) = (120, 240, 3)
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame to target size (240 width, 120 height)
        # Paper: Input shape is (30, 120, 240, 3), so each frame must be 120×240
        frame = cv2.resize(frame, self.target_size)
        
        # Convert from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
        # OpenCV uses BGR by default, but neural networks expect RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Neural networks train better with normalized inputs
        # Formula: normalized = original / 255.0
        frame = frame.astype(np.float32) / 255.0
        
        # Return processed frame ready for model input
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of consecutive frames from the video.
        
        Paper: Model input requires sequences of 30 frames (SEQUENCE_LENGTH = 30)
        This method extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            start_frame: Starting frame index (0-based, e.g., 0, 15, 30, ...)
            sequence_length: Number of frames to extract (default: 30)
            
        Returns:
            Sequence as numpy array with shape (sequence_length, height, width, channels)
            Example: (30, 120, 240, 3) for 30 frames of 120×240 RGB images
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        # Open video file using OpenCV
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # List to store extracted frames
        frames = []
        # Extract 'sequence_length' consecutive frames (default: 30 frames)
        for _ in range(sequence_length):
            # Read next frame from video
            # ret = True if frame read successfully, False if end of video
            # frame = the frame image (BGR format)
            ret, frame = cap.read()
            
            # If we reached end of video (no more frames available)
            if not ret:
                # Create a black frame (all zeros) with original video dimensions
                # This pads the sequence if video ends before we get 30 frames
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize frame to target size (240 width, 120 height)
            # Paper: Each frame must be 120×240 for model input
            frame = cv2.resize(frame, self.target_size)
            
            # Convert from BGR (OpenCV default) to RGB (neural network expects RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Normalize pixel values from [0, 255] to [0, 1] range
            # Formula: normalized = original / 255.0
            frame = frame.astype(np.float32) / 255.0
            
            # Add processed frame to the list
            frames.append(frame)
        
        # Release video capture to free resources
        cap.release()
        # Convert list of frames to NumPy array
        # Shape: (sequence_length, height, width, channels) = (30, 120, 240, 3)
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """Close all cached video captures."""
        for cap in self._video_captures.values():
            cap.release()
        self._video_captures.clear()


class UVPFLDataLoader:
    """
    Main data loader for UVPFL model.
    
    Provides:
    - Efficient data loading with on-demand frame extraction
    - Sequence creation for model input
    - Train/test split handling
    - Batch generation with prefetching
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence (default: 30)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second)
            batch_size: Batch size for training
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Load configuration
        self._load_config()
        
        # Load train/test split
        self._load_split()
        
        # Build sample index
        self._build_sample_index()
    
    def _load_config(self):
        """Load configuration from processed data."""
        config_path = self.processed_path / 'config.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.video_categories = self.config['video_categories']
        self.video_to_category = self.config['video_to_category']
        self.all_videos = self.config['all_videos']
        self.num_users = self.config['num_users']
    
    def _load_split(self):
        """Load train/test split."""
        split_path = self.processed_path / 'train_test_split.json'
        with open(split_path, 'r') as f:
            split = json.load(f)
        
        self.train_users = split['train_users']
        self.test_users = split['test_users']
    
    def _build_sample_index(self):
        """
        Build index of all available samples.
        Each sample is (video_name, user_id, start_frame, target_frame).
        """
        self.train_samples = []
        self.test_samples = []
        
        print("Building sample index...")
        
        for category, videos in self.video_categories.items():
            for video_name in videos:
                # Get frame count for this video
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Maximum start frame (need sequence_length + prediction_horizon frames)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count
                    orientation = np.load(orientation_path)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples (stride of 15 frames = 0.5 second to reduce redundancy)
                    stride = 15
                    for start_frame in range(0, actual_max_start, stride):
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        sample = {
                            'video_name': video_name,
                            'category': category,
                            'user_id': user_id,
                            'start_frame': start_frame,
                            'target_frame': target_frame
                        }
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """Load orientation data for a user-video pair."""
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single sample (frames sequence and target orientation).
        
        Args:
            sample: Sample dictionary with video_name, user_id, start_frame, target_frame
            
        Returns:
            Tuple of (frames_sequence, target_orientation)
            - frames_sequence: (sequence_length, height, width, channels)
            - target_orientation: (3,) = (yaw, pitch, roll)
        """
        video_name = sample['video_name']
        category = sample['category']
        user_id = sample['user_id']
        start_frame = sample['start_frame']
        target_frame = sample['target_frame']
        
        # Extract frame sequence
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation and get target
        orientation = self._load_orientation(video_name, category, user_id)
        target = orientation[target_frame]  # (yaw, pitch, roll)
        
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```

```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video at a specific index.
        
        Paper: Frames are extracted from saliency videos and resized to (120, 240, 3)
        for model input.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            frame_idx: Frame index (0-based, e.g., 0 = first frame, 1 = second frame)
            
        Returns:
            Frame as numpy array with shape (height, width, channels) = (120, 240, 3)
            Values normalized to [0, 1] range (for neural network training)
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        
        # Create new video capture object for each extraction (thread-safe approach)
        # This ensures each extraction is independent and doesn't interfere with others
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the desired frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Read the frame at that position
        # ret = True if frame was read successfully, False otherwise
        # frame = the actual frame image (BGR format)
        ret, frame = cap.read()
        # Release video capture to free resources
        cap.release()
        
        # If frame extraction failed (e.g., frame index out of bounds)
        if not ret:
            # Return a black frame (all zeros) with correct dimensions
            # Shape: (height, width, channels) = (120, 240, 3)
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame to target size (240 width, 120 height)
        # Paper: Input shape is (30, 120, 240, 3), so each frame must be 120×240
        frame = cv2.resize(frame, self.target_size)
        
        # Convert from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
        # OpenCV uses BGR by default, but neural networks expect RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Neural networks train better with normalized inputs
        # Formula: normalized = original / 255.0
        frame = frame.astype(np.float32) / 255.0
        
        # Return processed frame ready for model input
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of consecutive frames from the video.
        
        Paper: Model input requires sequences of 30 frames (SEQUENCE_LENGTH = 30)
        This method extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            start_frame: Starting frame index (0-based, e.g., 0, 15, 30, ...)
            sequence_length: Number of frames to extract (default: 30)
            
        Returns:
            Sequence as numpy array with shape (sequence_length, height, width, channels)
            Example: (30, 120, 240, 3) for 30 frames of 120×240 RGB images
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        # Open video file using OpenCV
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # List to store extracted frames
        frames = []
        # Extract 'sequence_length' consecutive frames (default: 30 frames)
        for _ in range(sequence_length):
            # Read next frame from video
            # ret = True if frame read successfully, False if end of video
            # frame = the frame image (BGR format)
            ret, frame = cap.read()
            
            # If we reached end of video (no more frames available)
            if not ret:
                # Create a black frame (all zeros) with original video dimensions
                # This pads the sequence if video ends before we get 30 frames
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize frame to target size (240 width, 120 height)
            # Paper: Each frame must be 120×240 for model input
            frame = cv2.resize(frame, self.target_size)
            
            # Convert from BGR (OpenCV default) to RGB (neural network expects RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Normalize pixel values from [0, 255] to [0, 1] range
            # Formula: normalized = original / 255.0
            frame = frame.astype(np.float32) / 255.0
            
            # Add processed frame to the list
            frames.append(frame)
        
        # Release video capture to free resources
        cap.release()
        # Convert list of frames to NumPy array
        # Shape: (sequence_length, height, width, channels) = (30, 120, 240, 3)
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """
        Close all cached video capture objects and free resources.
        
        This should be called when done using the extractor to properly
        release video file handles and free memory.
        """
        # Iterate through all cached video capture objects
        for cap in self._video_captures.values():
            # Release each video capture object (closes video file handle)
            cap.release()
        # Clear the cache dictionary (remove all entries)
        self._video_captures.clear()


class UVPFLDataLoader:
    """
    Main data loader for UVPFL model.
    
    Provides:
    - Efficient data loading with on-demand frame extraction
    - Sequence creation for model input
    - Train/test split handling
    - Batch generation with prefetching
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence (default: 30)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second)
            batch_size: Batch size for training
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Load configuration
        self._load_config()
        
        # Load train/test split
        self._load_split()
        
        # Build sample index
        self._build_sample_index()
    
    def _load_config(self):
        """Load configuration from processed data."""
        config_path = self.processed_path / 'config.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.video_categories = self.config['video_categories']
        self.video_to_category = self.config['video_to_category']
        self.all_videos = self.config['all_videos']
        self.num_users = self.config['num_users']
    
    def _load_split(self):
        """Load train/test split."""
        split_path = self.processed_path / 'train_test_split.json'
        with open(split_path, 'r') as f:
            split = json.load(f)
        
        self.train_users = split['train_users']
        self.test_users = split['test_users']
    
    def _build_sample_index(self):
        """
        Build index of all available samples.
        Each sample is (video_name, user_id, start_frame, target_frame).
        """
        self.train_samples = []
        self.test_samples = []
        
        print("Building sample index...")
        
        for category, videos in self.video_categories.items():
            for video_name in videos:
                # Get frame count for this video
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Maximum start frame (need sequence_length + prediction_horizon frames)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count
                    orientation = np.load(orientation_path)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples (stride of 15 frames = 0.5 second to reduce redundancy)
                    stride = 15
                    for start_frame in range(0, actual_max_start, stride):
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        sample = {
                            'video_name': video_name,
                            'category': category,
                            'user_id': user_id,
                            'start_frame': start_frame,
                            'target_frame': target_frame
                        }
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """Load orientation data for a user-video pair."""
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single sample (frames sequence and target orientation).
        
        Args:
            sample: Sample dictionary with video_name, user_id, start_frame, target_frame
            
        Returns:
            Tuple of (frames_sequence, target_orientation)
            - frames_sequence: (sequence_length, height, width, channels)
            - target_orientation: (3,) = (yaw, pitch, roll)
        """
        video_name = sample['video_name']
        category = sample['category']
        user_id = sample['user_id']
        start_frame = sample['start_frame']
        target_frame = sample['target_frame']
        
        # Extract frame sequence
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation and get target
        orientation = self._load_orientation(video_name, category, user_id)
        target = orientation[target_frame]  # (yaw, pitch, roll)
        
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```

```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video at a specific index.
        
        Paper: Frames are extracted from saliency videos and resized to (120, 240, 3)
        for model input.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            frame_idx: Frame index (0-based, e.g., 0 = first frame, 1 = second frame)
            
        Returns:
            Frame as numpy array with shape (height, width, channels) = (120, 240, 3)
            Values normalized to [0, 1] range (for neural network training)
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        
        # Create new video capture object for each extraction (thread-safe approach)
        # This ensures each extraction is independent and doesn't interfere with others
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the desired frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Read the frame at that position
        # ret = True if frame was read successfully, False otherwise
        # frame = the actual frame image (BGR format)
        ret, frame = cap.read()
        # Release video capture to free resources
        cap.release()
        
        # If frame extraction failed (e.g., frame index out of bounds)
        if not ret:
            # Return a black frame (all zeros) with correct dimensions
            # Shape: (height, width, channels) = (120, 240, 3)
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame to target size (240 width, 120 height)
        # Paper: Input shape is (30, 120, 240, 3), so each frame must be 120×240
        frame = cv2.resize(frame, self.target_size)
        
        # Convert from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
        # OpenCV uses BGR by default, but neural networks expect RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Neural networks train better with normalized inputs
        # Formula: normalized = original / 255.0
        frame = frame.astype(np.float32) / 255.0
        
        # Return processed frame ready for model input
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of consecutive frames from the video.
        
        Paper: Model input requires sequences of 30 frames (SEQUENCE_LENGTH = 30)
        This method extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            start_frame: Starting frame index (0-based, e.g., 0, 15, 30, ...)
            sequence_length: Number of frames to extract (default: 30)
            
        Returns:
            Sequence as numpy array with shape (sequence_length, height, width, channels)
            Example: (30, 120, 240, 3) for 30 frames of 120×240 RGB images
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        # Open video file using OpenCV
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # List to store extracted frames
        frames = []
        # Extract 'sequence_length' consecutive frames (default: 30 frames)
        for _ in range(sequence_length):
            # Read next frame from video
            # ret = True if frame read successfully, False if end of video
            # frame = the frame image (BGR format)
            ret, frame = cap.read()
            
            # If we reached end of video (no more frames available)
            if not ret:
                # Create a black frame (all zeros) with original video dimensions
                # This pads the sequence if video ends before we get 30 frames
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize frame to target size (240 width, 120 height)
            # Paper: Each frame must be 120×240 for model input
            frame = cv2.resize(frame, self.target_size)
            
            # Convert from BGR (OpenCV default) to RGB (neural network expects RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Normalize pixel values from [0, 255] to [0, 1] range
            # Formula: normalized = original / 255.0
            frame = frame.astype(np.float32) / 255.0
            
            # Add processed frame to the list
            frames.append(frame)
        
        # Release video capture to free resources
        cap.release()
        # Convert list of frames to NumPy array
        # Shape: (sequence_length, height, width, channels) = (30, 120, 240, 3)
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """
        Close all cached video capture objects and free resources.
        
        This should be called when done using the extractor to properly
        release video file handles and free memory.
        """
        # Iterate through all cached video capture objects
        for cap in self._video_captures.values():
            # Release each video capture object (closes video file handle)
            cap.release()
        # Clear the cache dictionary (remove all entries)
        self._video_captures.clear()


# ============================================================================
# UVPFL DATA LOADER CLASS (Main Data Loader)
# ============================================================================
class UVPFLDataLoader:
    """
    Main data loader for UVPFL model training and evaluation.
    
    This class provides:
    - Efficient data loading with on-demand frame extraction (saves memory)
    - Sequence creation for model input (30 frames per sequence)
    - Train/test split handling (separates users into train and test sets)
    - Batch generation with prefetching (optimizes GPU usage)
    
    Paper: Model input is sequences of 30 frames, predicting 1 second ahead (30 frames).
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader with dataset paths and configuration.
        
        Args:
            dataset_path: Path to original 360dataset folder (contains content/ and sensory/)
            processed_path: Path to processed data folder (created by data_preprocessing.py)
            sequence_length: Number of frames per sequence (default: 30, as per paper)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second at 30fps)
            batch_size: Number of samples per batch for training (default: 8)
        """
        # Store dataset paths as Path objects for easier file operations
        self.dataset_path = Path(dataset_path)  # Path to original dataset
        self.processed_path = Path(processed_path)  # Path to preprocessed data
        
        # Store model configuration parameters
        self.sequence_length = sequence_length  # 30 frames per sequence
        self.prediction_horizon = prediction_horizon  # Predict 30 frames ahead (1 second)
        self.batch_size = batch_size  # Number of samples per batch (e.g., 8)
        
        # Initialize frame extractor for on-demand frame extraction from videos
        # This extracts frames from saliency videos only when needed (memory efficient)
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'  # Path to saliency video folder
        )
        
        # Load configuration file (contains video categories, mappings, etc.)
        self._load_config()
        
        # Load train/test split (which users are for training vs testing)
        self._load_split()
        
        # Build index of all available samples (video, user, frame combinations)
        # This creates a list of all possible training/test samples
        self._build_sample_index()
    
    def _load_config(self):
        """Load configuration from processed data."""
        config_path = self.processed_path / 'config.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.video_categories = self.config['video_categories']
        self.video_to_category = self.config['video_to_category']
        self.all_videos = self.config['all_videos']
        self.num_users = self.config['num_users']
    
    def _load_split(self):
        """Load train/test split."""
        split_path = self.processed_path / 'train_test_split.json'
        with open(split_path, 'r') as f:
            split = json.load(f)
        
        self.train_users = split['train_users']
        self.test_users = split['test_users']
    
    def _build_sample_index(self):
        """
        Build index of all available samples.
        Each sample is (video_name, user_id, start_frame, target_frame).
        """
        self.train_samples = []
        self.test_samples = []
        
        print("Building sample index...")
        
        for category, videos in self.video_categories.items():
            for video_name in videos:
                # Get frame count for this video
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Maximum start frame (need sequence_length + prediction_horizon frames)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count
                    orientation = np.load(orientation_path)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples (stride of 15 frames = 0.5 second to reduce redundancy)
                    stride = 15
                    for start_frame in range(0, actual_max_start, stride):
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        sample = {
                            'video_name': video_name,
                            'category': category,
                            'user_id': user_id,
                            'start_frame': start_frame,
                            'target_frame': target_frame
                        }
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """Load orientation data for a user-video pair."""
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single sample (frames sequence and target orientation).
        
        Args:
            sample: Sample dictionary with video_name, user_id, start_frame, target_frame
            
        Returns:
            Tuple of (frames_sequence, target_orientation)
            - frames_sequence: (sequence_length, height, width, channels)
            - target_orientation: (3,) = (yaw, pitch, roll)
        """
        video_name = sample['video_name']
        category = sample['category']
        user_id = sample['user_id']
        start_frame = sample['start_frame']
        target_frame = sample['target_frame']
        
        # Extract frame sequence
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation and get target
        orientation = self._load_orientation(video_name, category, user_id)
        target = orientation[target_frame]  # (yaw, pitch, roll)
        
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```


Continuing with the helper methods. Adding comments to the remaining methods in batches:



Adding comments to the remaining methods in batches:


```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video at a specific index.
        
        Paper: Frames are extracted from saliency videos and resized to (120, 240, 3)
        for model input.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            frame_idx: Frame index (0-based, e.g., 0 = first frame, 1 = second frame)
            
        Returns:
            Frame as numpy array with shape (height, width, channels) = (120, 240, 3)
            Values normalized to [0, 1] range (for neural network training)
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        
        # Create new video capture object for each extraction (thread-safe approach)
        # This ensures each extraction is independent and doesn't interfere with others
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the desired frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Read the frame at that position
        # ret = True if frame was read successfully, False otherwise
        # frame = the actual frame image (BGR format)
        ret, frame = cap.read()
        # Release video capture to free resources
        cap.release()
        
        # If frame extraction failed (e.g., frame index out of bounds)
        if not ret:
            # Return a black frame (all zeros) with correct dimensions
            # Shape: (height, width, channels) = (120, 240, 3)
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame to target size (240 width, 120 height)
        # Paper: Input shape is (30, 120, 240, 3), so each frame must be 120×240
        frame = cv2.resize(frame, self.target_size)
        
        # Convert from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
        # OpenCV uses BGR by default, but neural networks expect RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Neural networks train better with normalized inputs
        # Formula: normalized = original / 255.0
        frame = frame.astype(np.float32) / 255.0
        
        # Return processed frame ready for model input
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of consecutive frames from the video.
        
        Paper: Model input requires sequences of 30 frames (SEQUENCE_LENGTH = 30)
        This method extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            start_frame: Starting frame index (0-based, e.g., 0, 15, 30, ...)
            sequence_length: Number of frames to extract (default: 30)
            
        Returns:
            Sequence as numpy array with shape (sequence_length, height, width, channels)
            Example: (30, 120, 240, 3) for 30 frames of 120×240 RGB images
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        # Open video file using OpenCV
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # List to store extracted frames
        frames = []
        # Extract 'sequence_length' consecutive frames (default: 30 frames)
        for _ in range(sequence_length):
            # Read next frame from video
            # ret = True if frame read successfully, False if end of video
            # frame = the frame image (BGR format)
            ret, frame = cap.read()
            
            # If we reached end of video (no more frames available)
            if not ret:
                # Create a black frame (all zeros) with original video dimensions
                # This pads the sequence if video ends before we get 30 frames
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize frame to target size (240 width, 120 height)
            # Paper: Each frame must be 120×240 for model input
            frame = cv2.resize(frame, self.target_size)
            
            # Convert from BGR (OpenCV default) to RGB (neural network expects RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Normalize pixel values from [0, 255] to [0, 1] range
            # Formula: normalized = original / 255.0
            frame = frame.astype(np.float32) / 255.0
            
            # Add processed frame to the list
            frames.append(frame)
        
        # Release video capture to free resources
        cap.release()
        # Convert list of frames to NumPy array
        # Shape: (sequence_length, height, width, channels) = (30, 120, 240, 3)
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """
        Close all cached video capture objects and free resources.
        
        This should be called when done using the extractor to properly
        release video file handles and free memory.
        """
        # Iterate through all cached video capture objects
        for cap in self._video_captures.values():
            # Release each video capture object (closes video file handle)
            cap.release()
        # Clear the cache dictionary (remove all entries)
        self._video_captures.clear()


# ============================================================================
# UVPFL DATA LOADER CLASS (Main Data Loader)
# ============================================================================
class UVPFLDataLoader:
    """
    Main data loader for UVPFL model training and evaluation.
    
    This class provides:
    - Efficient data loading with on-demand frame extraction (saves memory)
    - Sequence creation for model input (30 frames per sequence)
    - Train/test split handling (separates users into train and test sets)
    - Batch generation with prefetching (optimizes GPU usage)
    
    Paper: Model input is sequences of 30 frames, predicting 1 second ahead (30 frames).
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader with dataset paths and configuration.
        
        Args:
            dataset_path: Path to original 360dataset folder (contains content/ and sensory/)
            processed_path: Path to processed data folder (created by data_preprocessing.py)
            sequence_length: Number of frames per sequence (default: 30, as per paper)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second at 30fps)
            batch_size: Number of samples per batch for training (default: 8)
        """
        # Store dataset paths as Path objects for easier file operations
        self.dataset_path = Path(dataset_path)  # Path to original dataset
        self.processed_path = Path(processed_path)  # Path to preprocessed data
        
        # Store model configuration parameters
        self.sequence_length = sequence_length  # 30 frames per sequence
        self.prediction_horizon = prediction_horizon  # Predict 30 frames ahead (1 second)
        self.batch_size = batch_size  # Number of samples per batch (e.g., 8)
        
        # Initialize frame extractor for on-demand frame extraction from videos
        # This extracts frames from saliency videos only when needed (memory efficient)
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'  # Path to saliency video folder
        )
        
        # Load configuration file (contains video categories, mappings, etc.)
        self._load_config()
        
        # Load train/test split (which users are for training vs testing)
        self._load_split()
        
        # Build index of all available samples (video, user, frame combinations)
        # This creates a list of all possible training/test samples
        self._build_sample_index()
    
    def _load_config(self):
        """
        Load configuration file created by data_preprocessing.py.
        
        The config.json file contains:
        - video_categories: Mapping of categories to video lists
        - video_to_category: Reverse mapping (video name -> category)
        - all_videos: List of all video names
        - num_users: Total number of users (50)
        """
        # Path to configuration file (created during preprocessing)
        config_path = self.processed_path / 'config.json'
        # Open and read JSON configuration file
        with open(config_path, 'r') as f:
            self.config = json.load(f)  # Load entire config as dictionary
        
        # Extract configuration values for easy access
        self.video_categories = self.config['video_categories']  # e.g., {'cg_fast_paced': ['pacman', ...]}
        self.video_to_category = self.config['video_to_category']  # e.g., {'pacman': 'cg_fast_paced'}
        self.all_videos = self.config['all_videos']  # List of all 10 video names
        self.num_users = self.config['num_users']  # Total number of users (50)
    
    def _load_split(self):
        """
        Load train/test split created by data_preprocessing.py.
        
        The train_test_split.json file contains:
        - train_users: List of user IDs for training (40 users)
        - test_users: List of user IDs for testing (10 users)
        - seed: Random seed used for splitting (for reproducibility)
        """
        # Path to train/test split file (created during preprocessing)
        split_path = self.processed_path / 'train_test_split.json'
        # Open and read JSON split file
        with open(split_path, 'r') as f:
            split = json.load(f)  # Load split information as dictionary
        
        # Extract train and test user lists
        self.train_users = split['train_users']  # List of user IDs for training (e.g., [1, 2, 3, ..., 40])
        self.test_users = split['test_users']  # List of user IDs for testing (e.g., [41, 42, ..., 50])
    
    def _build_sample_index(self):
        """
        Build index of all available samples.
        Each sample is (video_name, user_id, start_frame, target_frame).
        """
        self.train_samples = []
        self.test_samples = []
        
        print("Building sample index...")
        
        for category, videos in self.video_categories.items():
            for video_name in videos:
                # Get frame count for this video
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Maximum start frame (need sequence_length + prediction_horizon frames)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count
                    orientation = np.load(orientation_path)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples (stride of 15 frames = 0.5 second to reduce redundancy)
                    stride = 15
                    for start_frame in range(0, actual_max_start, stride):
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        sample = {
                            'video_name': video_name,
                            'category': category,
                            'user_id': user_id,
                            'start_frame': start_frame,
                            'target_frame': target_frame
                        }
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """Load orientation data for a user-video pair."""
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single sample (frames sequence and target orientation).
        
        Args:
            sample: Sample dictionary with video_name, user_id, start_frame, target_frame
            
        Returns:
            Tuple of (frames_sequence, target_orientation)
            - frames_sequence: (sequence_length, height, width, channels)
            - target_orientation: (3,) = (yaw, pitch, roll)
        """
        video_name = sample['video_name']
        category = sample['category']
        user_id = sample['user_id']
        start_frame = sample['start_frame']
        target_frame = sample['target_frame']
        
        # Extract frame sequence
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation and get target
        orientation = self._load_orientation(video_name, category, user_id)
        target = orientation[target_frame]  # (yaw, pitch, roll)
        
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```


Adding detailed comments to `_build_sample_index` and the remaining methods. Creating a separate explanation document first, then finishing the comments:



Adding detailed comments to the remaining methods:


```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video at a specific index.
        
        Paper: Frames are extracted from saliency videos and resized to (120, 240, 3)
        for model input.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            frame_idx: Frame index (0-based, e.g., 0 = first frame, 1 = second frame)
            
        Returns:
            Frame as numpy array with shape (height, width, channels) = (120, 240, 3)
            Values normalized to [0, 1] range (for neural network training)
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        
        # Create new video capture object for each extraction (thread-safe approach)
        # This ensures each extraction is independent and doesn't interfere with others
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the desired frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Read the frame at that position
        # ret = True if frame was read successfully, False otherwise
        # frame = the actual frame image (BGR format)
        ret, frame = cap.read()
        # Release video capture to free resources
        cap.release()
        
        # If frame extraction failed (e.g., frame index out of bounds)
        if not ret:
            # Return a black frame (all zeros) with correct dimensions
            # Shape: (height, width, channels) = (120, 240, 3)
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame to target size (240 width, 120 height)
        # Paper: Input shape is (30, 120, 240, 3), so each frame must be 120×240
        frame = cv2.resize(frame, self.target_size)
        
        # Convert from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
        # OpenCV uses BGR by default, but neural networks expect RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Neural networks train better with normalized inputs
        # Formula: normalized = original / 255.0
        frame = frame.astype(np.float32) / 255.0
        
        # Return processed frame ready for model input
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of consecutive frames from the video.
        
        Paper: Model input requires sequences of 30 frames (SEQUENCE_LENGTH = 30)
        This method extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            start_frame: Starting frame index (0-based, e.g., 0, 15, 30, ...)
            sequence_length: Number of frames to extract (default: 30)
            
        Returns:
            Sequence as numpy array with shape (sequence_length, height, width, channels)
            Example: (30, 120, 240, 3) for 30 frames of 120×240 RGB images
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        # Open video file using OpenCV
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # List to store extracted frames
        frames = []
        # Extract 'sequence_length' consecutive frames (default: 30 frames)
        for _ in range(sequence_length):
            # Read next frame from video
            # ret = True if frame read successfully, False if end of video
            # frame = the frame image (BGR format)
            ret, frame = cap.read()
            
            # If we reached end of video (no more frames available)
            if not ret:
                # Create a black frame (all zeros) with original video dimensions
                # This pads the sequence if video ends before we get 30 frames
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize frame to target size (240 width, 120 height)
            # Paper: Each frame must be 120×240 for model input
            frame = cv2.resize(frame, self.target_size)
            
            # Convert from BGR (OpenCV default) to RGB (neural network expects RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Normalize pixel values from [0, 255] to [0, 1] range
            # Formula: normalized = original / 255.0
            frame = frame.astype(np.float32) / 255.0
            
            # Add processed frame to the list
            frames.append(frame)
        
        # Release video capture to free resources
        cap.release()
        # Convert list of frames to NumPy array
        # Shape: (sequence_length, height, width, channels) = (30, 120, 240, 3)
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """
        Close all cached video capture objects and free resources.
        
        This should be called when done using the extractor to properly
        release video file handles and free memory.
        """
        # Iterate through all cached video capture objects
        for cap in self._video_captures.values():
            # Release each video capture object (closes video file handle)
            cap.release()
        # Clear the cache dictionary (remove all entries)
        self._video_captures.clear()


# ============================================================================
# UVPFL DATA LOADER CLASS (Main Data Loader)
# ============================================================================
class UVPFLDataLoader:
    """
    Main data loader for UVPFL model training and evaluation.
    
    This class provides:
    - Efficient data loading with on-demand frame extraction (saves memory)
    - Sequence creation for model input (30 frames per sequence)
    - Train/test split handling (separates users into train and test sets)
    - Batch generation with prefetching (optimizes GPU usage)
    
    Paper: Model input is sequences of 30 frames, predicting 1 second ahead (30 frames).
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader with dataset paths and configuration.
        
        Args:
            dataset_path: Path to original 360dataset folder (contains content/ and sensory/)
            processed_path: Path to processed data folder (created by data_preprocessing.py)
            sequence_length: Number of frames per sequence (default: 30, as per paper)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second at 30fps)
            batch_size: Number of samples per batch for training (default: 8)
        """
        # Store dataset paths as Path objects for easier file operations
        self.dataset_path = Path(dataset_path)  # Path to original dataset
        self.processed_path = Path(processed_path)  # Path to preprocessed data
        
        # Store model configuration parameters
        self.sequence_length = sequence_length  # 30 frames per sequence
        self.prediction_horizon = prediction_horizon  # Predict 30 frames ahead (1 second)
        self.batch_size = batch_size  # Number of samples per batch (e.g., 8)
        
        # Initialize frame extractor for on-demand frame extraction from videos
        # This extracts frames from saliency videos only when needed (memory efficient)
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'  # Path to saliency video folder
        )
        
        # Load configuration file (contains video categories, mappings, etc.)
        self._load_config()
        
        # Load train/test split (which users are for training vs testing)
        self._load_split()
        
        # Build index of all available samples (video, user, frame combinations)
        # This creates a list of all possible training/test samples
        self._build_sample_index()
    
    def _load_config(self):
        """
        Load configuration file created by data_preprocessing.py.
        
        The config.json file contains:
        - video_categories: Mapping of categories to video lists
        - video_to_category: Reverse mapping (video name -> category)
        - all_videos: List of all video names
        - num_users: Total number of users (50)
        """
        # Path to configuration file (created during preprocessing)
        config_path = self.processed_path / 'config.json'
        # Open and read JSON configuration file
        with open(config_path, 'r') as f:
            self.config = json.load(f)  # Load entire config as dictionary
        
        # Extract configuration values for easy access
        self.video_categories = self.config['video_categories']  # e.g., {'cg_fast_paced': ['pacman', ...]}
        self.video_to_category = self.config['video_to_category']  # e.g., {'pacman': 'cg_fast_paced'}
        self.all_videos = self.config['all_videos']  # List of all 10 video names
        self.num_users = self.config['num_users']  # Total number of users (50)
    
    def _load_split(self):
        """
        Load train/test split created by data_preprocessing.py.
        
        The train_test_split.json file contains:
        - train_users: List of user IDs for training (40 users)
        - test_users: List of user IDs for testing (10 users)
        - seed: Random seed used for splitting (for reproducibility)
        """
        # Path to train/test split file (created during preprocessing)
        split_path = self.processed_path / 'train_test_split.json'
        # Open and read JSON split file
        with open(split_path, 'r') as f:
            split = json.load(f)  # Load split information as dictionary
        
        # Extract train and test user lists
        self.train_users = split['train_users']  # List of user IDs for training (e.g., [1, 2, 3, ..., 40])
        self.test_users = split['test_users']  # List of user IDs for testing (e.g., [41, 42, ..., 50])
    
    def _build_sample_index(self):
        """
        Build index of all available training and test samples.
        
        A sample represents one training example:
        - Input: 30 consecutive frames (sequence_length = 30)
        - Target: Orientation (Y, PI, R) at frame (start_frame + 30 + 30 - 1)
        
        Example:
        - start_frame = 0: Use frames 0-29 → predict frame 59 (1 second ahead)
        - start_frame = 15: Use frames 15-44 → predict frame 74 (1 second ahead)
        
        This method creates all possible samples by:
        1. Iterating through all videos and users
        2. Creating samples with stride of 15 frames (0.5 seconds) to reduce redundancy
        3. Separating samples into train/test based on user ID
        """
        # Initialize empty lists to store sample dictionaries
        self.train_samples = []  # List of training samples (dictionaries)
        self.test_samples = []  # List of test samples (dictionaries)
        
        print("Building sample index...")
        
        # Iterate through each video category (cg_fast_paced, ni_fast_paced, ni_slow_paced)
        for category, videos in self.video_categories.items():
            # Iterate through each video in this category
            for video_name in videos:
                # Get total number of frames in this video (from saliency video file)
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Calculate maximum starting frame index
                # We need: sequence_length (30) frames + prediction_horizon (30) frames
                # Formula: max_start = frame_count - 30 - 30 = frame_count - 60
                # Example: If video has 1800 frames, max_start = 1800 - 60 = 1740
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                # Skip this video if it's too short (can't create any samples)
                if max_start <= 0:
                    continue
                
                # Iterate through all users (1 to 50)
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists for this user-video pair
                    # Path: processed_data/category/video/userXX/orientation.npy
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    # Skip this user if orientation data doesn't exist
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count for this user
                    # (Some users may have fewer frames due to incomplete data)
                    orientation = np.load(orientation_path)
                    # Calculate actual maximum start frame (use minimum of video frames and user frames)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    # Skip if can't create any samples for this user
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples with stride of 15 frames (0.5 seconds)
                    # This reduces redundancy: samples at 0, 15, 30, 45, ... instead of 0, 1, 2, 3, ...
                    # Stride of 15 means we create a sample every 0.5 seconds
                    stride = 15
                    # Iterate through possible start frames: 0, 15, 30, 45, ..., actual_max_start
                    for start_frame in range(0, actual_max_start, stride):
                        # Calculate target frame index
                        # target_frame = start_frame + sequence_length + prediction_horizon - 1
                        # Example: start_frame=0 → target_frame = 0 + 30 + 30 - 1 = 59
                        # This means: use frames 0-29 to predict frame 59 (1 second ahead)
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        # Create sample dictionary with all necessary information
                        sample = {
                            'video_name': video_name,  # e.g., 'coaster'
                            'category': category,  # e.g., 'ni_fast_paced'
                            'user_id': user_id,  # e.g., 5
                            'start_frame': start_frame,  # e.g., 0
                            'target_frame': target_frame  # e.g., 59
                        }
                        
                        # Add sample to appropriate list based on user ID
                        if user_id in self.train_users:
                            self.train_samples.append(sample)  # Add to training set
                        else:
                            self.test_samples.append(sample)  # Add to test set
        
        # Print summary of created samples
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """Load orientation data for a user-video pair."""
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single sample (frames sequence and target orientation).
        
        Args:
            sample: Sample dictionary with video_name, user_id, start_frame, target_frame
            
        Returns:
            Tuple of (frames_sequence, target_orientation)
            - frames_sequence: (sequence_length, height, width, channels)
            - target_orientation: (3,) = (yaw, pitch, roll)
        """
        video_name = sample['video_name']
        category = sample['category']
        user_id = sample['user_id']
        start_frame = sample['start_frame']
        target_frame = sample['target_frame']
        
        # Extract frame sequence
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation and get target
        orientation = self._load_orientation(video_name, category, user_id)
        target = orientation[target_frame]  # (yaw, pitch, roll)
        
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```


Adding comments to the remaining key methods:


```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video at a specific index.
        
        Paper: Frames are extracted from saliency videos and resized to (120, 240, 3)
        for model input.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            frame_idx: Frame index (0-based, e.g., 0 = first frame, 1 = second frame)
            
        Returns:
            Frame as numpy array with shape (height, width, channels) = (120, 240, 3)
            Values normalized to [0, 1] range (for neural network training)
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        
        # Create new video capture object for each extraction (thread-safe approach)
        # This ensures each extraction is independent and doesn't interfere with others
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the desired frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Read the frame at that position
        # ret = True if frame was read successfully, False otherwise
        # frame = the actual frame image (BGR format)
        ret, frame = cap.read()
        # Release video capture to free resources
        cap.release()
        
        # If frame extraction failed (e.g., frame index out of bounds)
        if not ret:
            # Return a black frame (all zeros) with correct dimensions
            # Shape: (height, width, channels) = (120, 240, 3)
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame to target size (240 width, 120 height)
        # Paper: Input shape is (30, 120, 240, 3), so each frame must be 120×240
        frame = cv2.resize(frame, self.target_size)
        
        # Convert from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
        # OpenCV uses BGR by default, but neural networks expect RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Neural networks train better with normalized inputs
        # Formula: normalized = original / 255.0
        frame = frame.astype(np.float32) / 255.0
        
        # Return processed frame ready for model input
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of consecutive frames from the video.
        
        Paper: Model input requires sequences of 30 frames (SEQUENCE_LENGTH = 30)
        This method extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            start_frame: Starting frame index (0-based, e.g., 0, 15, 30, ...)
            sequence_length: Number of frames to extract (default: 30)
            
        Returns:
            Sequence as numpy array with shape (sequence_length, height, width, channels)
            Example: (30, 120, 240, 3) for 30 frames of 120×240 RGB images
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        # Open video file using OpenCV
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # List to store extracted frames
        frames = []
        # Extract 'sequence_length' consecutive frames (default: 30 frames)
        for _ in range(sequence_length):
            # Read next frame from video
            # ret = True if frame read successfully, False if end of video
            # frame = the frame image (BGR format)
            ret, frame = cap.read()
            
            # If we reached end of video (no more frames available)
            if not ret:
                # Create a black frame (all zeros) with original video dimensions
                # This pads the sequence if video ends before we get 30 frames
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize frame to target size (240 width, 120 height)
            # Paper: Each frame must be 120×240 for model input
            frame = cv2.resize(frame, self.target_size)
            
            # Convert from BGR (OpenCV default) to RGB (neural network expects RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Normalize pixel values from [0, 255] to [0, 1] range
            # Formula: normalized = original / 255.0
            frame = frame.astype(np.float32) / 255.0
            
            # Add processed frame to the list
            frames.append(frame)
        
        # Release video capture to free resources
        cap.release()
        # Convert list of frames to NumPy array
        # Shape: (sequence_length, height, width, channels) = (30, 120, 240, 3)
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """
        Close all cached video capture objects and free resources.
        
        This should be called when done using the extractor to properly
        release video file handles and free memory.
        """
        # Iterate through all cached video capture objects
        for cap in self._video_captures.values():
            # Release each video capture object (closes video file handle)
            cap.release()
        # Clear the cache dictionary (remove all entries)
        self._video_captures.clear()


# ============================================================================
# UVPFL DATA LOADER CLASS (Main Data Loader)
# ============================================================================
class UVPFLDataLoader:
    """
    Main data loader for UVPFL model training and evaluation.
    
    This class provides:
    - Efficient data loading with on-demand frame extraction (saves memory)
    - Sequence creation for model input (30 frames per sequence)
    - Train/test split handling (separates users into train and test sets)
    - Batch generation with prefetching (optimizes GPU usage)
    
    Paper: Model input is sequences of 30 frames, predicting 1 second ahead (30 frames).
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader with dataset paths and configuration.
        
        Args:
            dataset_path: Path to original 360dataset folder (contains content/ and sensory/)
            processed_path: Path to processed data folder (created by data_preprocessing.py)
            sequence_length: Number of frames per sequence (default: 30, as per paper)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second at 30fps)
            batch_size: Number of samples per batch for training (default: 8)
        """
        # Store dataset paths as Path objects for easier file operations
        self.dataset_path = Path(dataset_path)  # Path to original dataset
        self.processed_path = Path(processed_path)  # Path to preprocessed data
        
        # Store model configuration parameters
        self.sequence_length = sequence_length  # 30 frames per sequence
        self.prediction_horizon = prediction_horizon  # Predict 30 frames ahead (1 second)
        self.batch_size = batch_size  # Number of samples per batch (e.g., 8)
        
        # Initialize frame extractor for on-demand frame extraction from videos
        # This extracts frames from saliency videos only when needed (memory efficient)
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'  # Path to saliency video folder
        )
        
        # Load configuration file (contains video categories, mappings, etc.)
        self._load_config()
        
        # Load train/test split (which users are for training vs testing)
        self._load_split()
        
        # Build index of all available samples (video, user, frame combinations)
        # This creates a list of all possible training/test samples
        self._build_sample_index()
    
    def _load_config(self):
        """
        Load configuration file created by data_preprocessing.py.
        
        The config.json file contains:
        - video_categories: Mapping of categories to video lists
        - video_to_category: Reverse mapping (video name -> category)
        - all_videos: List of all video names
        - num_users: Total number of users (50)
        """
        # Path to configuration file (created during preprocessing)
        config_path = self.processed_path / 'config.json'
        # Open and read JSON configuration file
        with open(config_path, 'r') as f:
            self.config = json.load(f)  # Load entire config as dictionary
        
        # Extract configuration values for easy access
        self.video_categories = self.config['video_categories']  # e.g., {'cg_fast_paced': ['pacman', ...]}
        self.video_to_category = self.config['video_to_category']  # e.g., {'pacman': 'cg_fast_paced'}
        self.all_videos = self.config['all_videos']  # List of all 10 video names
        self.num_users = self.config['num_users']  # Total number of users (50)
    
    def _load_split(self):
        """
        Load train/test split created by data_preprocessing.py.
        
        The train_test_split.json file contains:
        - train_users: List of user IDs for training (40 users)
        - test_users: List of user IDs for testing (10 users)
        - seed: Random seed used for splitting (for reproducibility)
        """
        # Path to train/test split file (created during preprocessing)
        split_path = self.processed_path / 'train_test_split.json'
        # Open and read JSON split file
        with open(split_path, 'r') as f:
            split = json.load(f)  # Load split information as dictionary
        
        # Extract train and test user lists
        self.train_users = split['train_users']  # List of user IDs for training (e.g., [1, 2, 3, ..., 40])
        self.test_users = split['test_users']  # List of user IDs for testing (e.g., [41, 42, ..., 50])
    
    def _build_sample_index(self):
        """
        Build index of all available training and test samples.
        
        A sample represents one training example:
        - Input: 30 consecutive frames (sequence_length = 30)
        - Target: Orientation (Y, PI, R) at frame (start_frame + 30 + 30 - 1)
        
        Example:
        - start_frame = 0: Use frames 0-29 → predict frame 59 (1 second ahead)
        - start_frame = 15: Use frames 15-44 → predict frame 74 (1 second ahead)
        
        This method creates all possible samples by:
        1. Iterating through all videos and users
        2. Creating samples with stride of 15 frames (0.5 seconds) to reduce redundancy
        3. Separating samples into train/test based on user ID
        """
        # Initialize empty lists to store sample dictionaries
        self.train_samples = []  # List of training samples (dictionaries)
        self.test_samples = []  # List of test samples (dictionaries)
        
        print("Building sample index...")
        
        # Iterate through each video category (cg_fast_paced, ni_fast_paced, ni_slow_paced)
        for category, videos in self.video_categories.items():
            # Iterate through each video in this category
            for video_name in videos:
                # Get total number of frames in this video (from saliency video file)
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Calculate maximum starting frame index
                # We need: sequence_length (30) frames + prediction_horizon (30) frames
                # Formula: max_start = frame_count - 30 - 30 = frame_count - 60
                # Example: If video has 1800 frames, max_start = 1800 - 60 = 1740
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                # Skip this video if it's too short (can't create any samples)
                if max_start <= 0:
                    continue
                
                # Iterate through all users (1 to 50)
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists for this user-video pair
                    # Path: processed_data/category/video/userXX/orientation.npy
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    # Skip this user if orientation data doesn't exist
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count for this user
                    # (Some users may have fewer frames due to incomplete data)
                    orientation = np.load(orientation_path)
                    # Calculate actual maximum start frame (use minimum of video frames and user frames)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    # Skip if can't create any samples for this user
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples with stride of 15 frames (0.5 seconds)
                    # This reduces redundancy: samples at 0, 15, 30, 45, ... instead of 0, 1, 2, 3, ...
                    # Stride of 15 means we create a sample every 0.5 seconds
                    stride = 15
                    # Iterate through possible start frames: 0, 15, 30, 45, ..., actual_max_start
                    for start_frame in range(0, actual_max_start, stride):
                        # Calculate target frame index
                        # target_frame = start_frame + sequence_length + prediction_horizon - 1
                        # Example: start_frame=0 → target_frame = 0 + 30 + 30 - 1 = 59
                        # This means: use frames 0-29 to predict frame 59 (1 second ahead)
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        # Create sample dictionary with all necessary information
                        sample = {
                            'video_name': video_name,  # e.g., 'coaster'
                            'category': category,  # e.g., 'ni_fast_paced'
                            'user_id': user_id,  # e.g., 5
                            'start_frame': start_frame,  # e.g., 0
                            'target_frame': target_frame  # e.g., 59
                        }
                        
                        # Add sample to appropriate list based on user ID
                        if user_id in self.train_users:
                            self.train_samples.append(sample)  # Add to training set
                        else:
                            self.test_samples.append(sample)  # Add to test set
        
        # Print summary of created samples
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """
        Load orientation data (Y, PI, R angles) for a specific user-video pair.
        
        Paper: Target is (Y, PI, R) = (Yaw, Pitch, Roll) angles for each frame.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            category: Video category (e.g., 'ni_fast_paced')
            user_id: User ID (1-50)
            
        Returns:
            NumPy array with shape (num_frames, 3) containing [yaw, pitch, roll] for each frame
        """
        # Construct path to orientation file: processed_data/category/video/userXX/orientation.npy
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        # Load NumPy array from file (created by data_preprocessing.py)
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single training sample: extract frames and get target orientation.
        
        This is the core method that creates one training example:
        - Input: 30 consecutive frames from saliency video
        - Target: Orientation (Y, PI, R) at the prediction frame
        
        Paper: Model input is (30, 120, 240, 3) and target is (3,) = (yaw, pitch, roll)
        
        Args:
            sample: Sample dictionary containing:
                - video_name: Name of the video
                - category: Video category
                - user_id: User ID
                - start_frame: Starting frame index for sequence
                - target_frame: Frame index to predict (1 second ahead)
            
        Returns:
            Tuple of (frames_sequence, target_orientation):
            - frames_sequence: NumPy array with shape (30, 120, 240, 3) - 30 frames of 120×240 RGB images
            - target_orientation: NumPy array with shape (3,) = [yaw, pitch, roll] angles
        """
        # Extract information from sample dictionary
        video_name = sample['video_name']  # e.g., 'coaster'
        category = sample['category']  # e.g., 'ni_fast_paced'
        user_id = sample['user_id']  # e.g., 5
        start_frame = sample['start_frame']  # e.g., 0 (start of sequence)
        target_frame = sample['target_frame']  # e.g., 59 (frame to predict)
        
        # Extract sequence of 30 consecutive frames from saliency video
        # This calls VideoFrameExtractor.extract_sequence() which:
        # 1. Opens video file
        # 2. Extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        # 3. Resizes each frame to 120×240
        # 4. Converts BGR to RGB
        # 5. Normalizes to [0, 1]
        # Returns: (30, 120, 240, 3) array
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation data for this user-video pair
        # Returns: (num_frames, 3) array with [yaw, pitch, roll] for each frame
        orientation = self._load_orientation(video_name, category, user_id)
        
        # Get target orientation at the prediction frame
        # target_frame is calculated as: start_frame + 30 + 30 - 1 = start_frame + 59
        # This gives us the orientation 1 second (30 frames) ahead
        target = orientation[target_frame]  # Extract [yaw, pitch, roll] at target_frame
        
        # Return frames and target, converting target to float32 for neural network
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Generator that yields samples one at a time.
        
        Args:
            samples: List of sample dictionaries
            shuffle: Whether to shuffle samples
            
        Yields:
            Tuple of (frames, target)
        """
        indices = np.arange(len(samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for idx in indices:
                sample = samples[idx]
                try:
                    frames, target = self._get_sample(sample)
                    yield frames, target
                except Exception as e:
                    # Skip problematic samples
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient training.
        
        Args:
            split: 'train' or 'test'
            shuffle: Whether to shuffle data
            prefetch: Whether to prefetch batches
            
        Returns:
            tf.data.Dataset
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Output signature
        output_signature = (
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create dataset from generator
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),
            output_signature=output_signature
        )
        
        # Batch
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch for GPU efficiency
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```


Adding comments to the data generator and TensorFlow dataset methods:


```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video at a specific index.
        
        Paper: Frames are extracted from saliency videos and resized to (120, 240, 3)
        for model input.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            frame_idx: Frame index (0-based, e.g., 0 = first frame, 1 = second frame)
            
        Returns:
            Frame as numpy array with shape (height, width, channels) = (120, 240, 3)
            Values normalized to [0, 1] range (for neural network training)
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        
        # Create new video capture object for each extraction (thread-safe approach)
        # This ensures each extraction is independent and doesn't interfere with others
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the desired frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Read the frame at that position
        # ret = True if frame was read successfully, False otherwise
        # frame = the actual frame image (BGR format)
        ret, frame = cap.read()
        # Release video capture to free resources
        cap.release()
        
        # If frame extraction failed (e.g., frame index out of bounds)
        if not ret:
            # Return a black frame (all zeros) with correct dimensions
            # Shape: (height, width, channels) = (120, 240, 3)
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame to target size (240 width, 120 height)
        # Paper: Input shape is (30, 120, 240, 3), so each frame must be 120×240
        frame = cv2.resize(frame, self.target_size)
        
        # Convert from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
        # OpenCV uses BGR by default, but neural networks expect RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Neural networks train better with normalized inputs
        # Formula: normalized = original / 255.0
        frame = frame.astype(np.float32) / 255.0
        
        # Return processed frame ready for model input
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of consecutive frames from the video.
        
        Paper: Model input requires sequences of 30 frames (SEQUENCE_LENGTH = 30)
        This method extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            start_frame: Starting frame index (0-based, e.g., 0, 15, 30, ...)
            sequence_length: Number of frames to extract (default: 30)
            
        Returns:
            Sequence as numpy array with shape (sequence_length, height, width, channels)
            Example: (30, 120, 240, 3) for 30 frames of 120×240 RGB images
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        # Open video file using OpenCV
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # List to store extracted frames
        frames = []
        # Extract 'sequence_length' consecutive frames (default: 30 frames)
        for _ in range(sequence_length):
            # Read next frame from video
            # ret = True if frame read successfully, False if end of video
            # frame = the frame image (BGR format)
            ret, frame = cap.read()
            
            # If we reached end of video (no more frames available)
            if not ret:
                # Create a black frame (all zeros) with original video dimensions
                # This pads the sequence if video ends before we get 30 frames
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize frame to target size (240 width, 120 height)
            # Paper: Each frame must be 120×240 for model input
            frame = cv2.resize(frame, self.target_size)
            
            # Convert from BGR (OpenCV default) to RGB (neural network expects RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Normalize pixel values from [0, 255] to [0, 1] range
            # Formula: normalized = original / 255.0
            frame = frame.astype(np.float32) / 255.0
            
            # Add processed frame to the list
            frames.append(frame)
        
        # Release video capture to free resources
        cap.release()
        # Convert list of frames to NumPy array
        # Shape: (sequence_length, height, width, channels) = (30, 120, 240, 3)
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """
        Close all cached video capture objects and free resources.
        
        This should be called when done using the extractor to properly
        release video file handles and free memory.
        """
        # Iterate through all cached video capture objects
        for cap in self._video_captures.values():
            # Release each video capture object (closes video file handle)
            cap.release()
        # Clear the cache dictionary (remove all entries)
        self._video_captures.clear()


# ============================================================================
# UVPFL DATA LOADER CLASS (Main Data Loader)
# ============================================================================
class UVPFLDataLoader:
    """
    Main data loader for UVPFL model training and evaluation.
    
    This class provides:
    - Efficient data loading with on-demand frame extraction (saves memory)
    - Sequence creation for model input (30 frames per sequence)
    - Train/test split handling (separates users into train and test sets)
    - Batch generation with prefetching (optimizes GPU usage)
    
    Paper: Model input is sequences of 30 frames, predicting 1 second ahead (30 frames).
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader with dataset paths and configuration.
        
        Args:
            dataset_path: Path to original 360dataset folder (contains content/ and sensory/)
            processed_path: Path to processed data folder (created by data_preprocessing.py)
            sequence_length: Number of frames per sequence (default: 30, as per paper)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second at 30fps)
            batch_size: Number of samples per batch for training (default: 8)
        """
        # Store dataset paths as Path objects for easier file operations
        self.dataset_path = Path(dataset_path)  # Path to original dataset
        self.processed_path = Path(processed_path)  # Path to preprocessed data
        
        # Store model configuration parameters
        self.sequence_length = sequence_length  # 30 frames per sequence
        self.prediction_horizon = prediction_horizon  # Predict 30 frames ahead (1 second)
        self.batch_size = batch_size  # Number of samples per batch (e.g., 8)
        
        # Initialize frame extractor for on-demand frame extraction from videos
        # This extracts frames from saliency videos only when needed (memory efficient)
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'  # Path to saliency video folder
        )
        
        # Load configuration file (contains video categories, mappings, etc.)
        self._load_config()
        
        # Load train/test split (which users are for training vs testing)
        self._load_split()
        
        # Build index of all available samples (video, user, frame combinations)
        # This creates a list of all possible training/test samples
        self._build_sample_index()
    
    def _load_config(self):
        """
        Load configuration file created by data_preprocessing.py.
        
        The config.json file contains:
        - video_categories: Mapping of categories to video lists
        - video_to_category: Reverse mapping (video name -> category)
        - all_videos: List of all video names
        - num_users: Total number of users (50)
        """
        # Path to configuration file (created during preprocessing)
        config_path = self.processed_path / 'config.json'
        # Open and read JSON configuration file
        with open(config_path, 'r') as f:
            self.config = json.load(f)  # Load entire config as dictionary
        
        # Extract configuration values for easy access
        self.video_categories = self.config['video_categories']  # e.g., {'cg_fast_paced': ['pacman', ...]}
        self.video_to_category = self.config['video_to_category']  # e.g., {'pacman': 'cg_fast_paced'}
        self.all_videos = self.config['all_videos']  # List of all 10 video names
        self.num_users = self.config['num_users']  # Total number of users (50)
    
    def _load_split(self):
        """
        Load train/test split created by data_preprocessing.py.
        
        The train_test_split.json file contains:
        - train_users: List of user IDs for training (40 users)
        - test_users: List of user IDs for testing (10 users)
        - seed: Random seed used for splitting (for reproducibility)
        """
        # Path to train/test split file (created during preprocessing)
        split_path = self.processed_path / 'train_test_split.json'
        # Open and read JSON split file
        with open(split_path, 'r') as f:
            split = json.load(f)  # Load split information as dictionary
        
        # Extract train and test user lists
        self.train_users = split['train_users']  # List of user IDs for training (e.g., [1, 2, 3, ..., 40])
        self.test_users = split['test_users']  # List of user IDs for testing (e.g., [41, 42, ..., 50])
    
    def _build_sample_index(self):
        """
        Build index of all available training and test samples.
        
        A sample represents one training example:
        - Input: 30 consecutive frames (sequence_length = 30)
        - Target: Orientation (Y, PI, R) at frame (start_frame + 30 + 30 - 1)
        
        Example:
        - start_frame = 0: Use frames 0-29 → predict frame 59 (1 second ahead)
        - start_frame = 15: Use frames 15-44 → predict frame 74 (1 second ahead)
        
        This method creates all possible samples by:
        1. Iterating through all videos and users
        2. Creating samples with stride of 15 frames (0.5 seconds) to reduce redundancy
        3. Separating samples into train/test based on user ID
        """
        # Initialize empty lists to store sample dictionaries
        self.train_samples = []  # List of training samples (dictionaries)
        self.test_samples = []  # List of test samples (dictionaries)
        
        print("Building sample index...")
        
        # Iterate through each video category (cg_fast_paced, ni_fast_paced, ni_slow_paced)
        for category, videos in self.video_categories.items():
            # Iterate through each video in this category
            for video_name in videos:
                # Get total number of frames in this video (from saliency video file)
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Calculate maximum starting frame index
                # We need: sequence_length (30) frames + prediction_horizon (30) frames
                # Formula: max_start = frame_count - 30 - 30 = frame_count - 60
                # Example: If video has 1800 frames, max_start = 1800 - 60 = 1740
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                # Skip this video if it's too short (can't create any samples)
                if max_start <= 0:
                    continue
                
                # Iterate through all users (1 to 50)
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists for this user-video pair
                    # Path: processed_data/category/video/userXX/orientation.npy
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    # Skip this user if orientation data doesn't exist
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count for this user
                    # (Some users may have fewer frames due to incomplete data)
                    orientation = np.load(orientation_path)
                    # Calculate actual maximum start frame (use minimum of video frames and user frames)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    # Skip if can't create any samples for this user
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples with stride of 15 frames (0.5 seconds)
                    # This reduces redundancy: samples at 0, 15, 30, 45, ... instead of 0, 1, 2, 3, ...
                    # Stride of 15 means we create a sample every 0.5 seconds
                    stride = 15
                    # Iterate through possible start frames: 0, 15, 30, 45, ..., actual_max_start
                    for start_frame in range(0, actual_max_start, stride):
                        # Calculate target frame index
                        # target_frame = start_frame + sequence_length + prediction_horizon - 1
                        # Example: start_frame=0 → target_frame = 0 + 30 + 30 - 1 = 59
                        # This means: use frames 0-29 to predict frame 59 (1 second ahead)
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        # Create sample dictionary with all necessary information
                        sample = {
                            'video_name': video_name,  # e.g., 'coaster'
                            'category': category,  # e.g., 'ni_fast_paced'
                            'user_id': user_id,  # e.g., 5
                            'start_frame': start_frame,  # e.g., 0
                            'target_frame': target_frame  # e.g., 59
                        }
                        
                        # Add sample to appropriate list based on user ID
                        if user_id in self.train_users:
                            self.train_samples.append(sample)  # Add to training set
                        else:
                            self.test_samples.append(sample)  # Add to test set
        
        # Print summary of created samples
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """
        Load orientation data (Y, PI, R angles) for a specific user-video pair.
        
        Paper: Target is (Y, PI, R) = (Yaw, Pitch, Roll) angles for each frame.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            category: Video category (e.g., 'ni_fast_paced')
            user_id: User ID (1-50)
            
        Returns:
            NumPy array with shape (num_frames, 3) containing [yaw, pitch, roll] for each frame
        """
        # Construct path to orientation file: processed_data/category/video/userXX/orientation.npy
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        # Load NumPy array from file (created by data_preprocessing.py)
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single training sample: extract frames and get target orientation.
        
        This is the core method that creates one training example:
        - Input: 30 consecutive frames from saliency video
        - Target: Orientation (Y, PI, R) at the prediction frame
        
        Paper: Model input is (30, 120, 240, 3) and target is (3,) = (yaw, pitch, roll)
        
        Args:
            sample: Sample dictionary containing:
                - video_name: Name of the video
                - category: Video category
                - user_id: User ID
                - start_frame: Starting frame index for sequence
                - target_frame: Frame index to predict (1 second ahead)
            
        Returns:
            Tuple of (frames_sequence, target_orientation):
            - frames_sequence: NumPy array with shape (30, 120, 240, 3) - 30 frames of 120×240 RGB images
            - target_orientation: NumPy array with shape (3,) = [yaw, pitch, roll] angles
        """
        # Extract information from sample dictionary
        video_name = sample['video_name']  # e.g., 'coaster'
        category = sample['category']  # e.g., 'ni_fast_paced'
        user_id = sample['user_id']  # e.g., 5
        start_frame = sample['start_frame']  # e.g., 0 (start of sequence)
        target_frame = sample['target_frame']  # e.g., 59 (frame to predict)
        
        # Extract sequence of 30 consecutive frames from saliency video
        # This calls VideoFrameExtractor.extract_sequence() which:
        # 1. Opens video file
        # 2. Extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        # 3. Resizes each frame to 120×240
        # 4. Converts BGR to RGB
        # 5. Normalizes to [0, 1]
        # Returns: (30, 120, 240, 3) array
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation data for this user-video pair
        # Returns: (num_frames, 3) array with [yaw, pitch, roll] for each frame
        orientation = self._load_orientation(video_name, category, user_id)
        
        # Get target orientation at the prediction frame
        # target_frame is calculated as: start_frame + 30 + 30 - 1 = start_frame + 59
        # This gives us the orientation 1 second (30 frames) ahead
        target = orientation[target_frame]  # Extract [yaw, pitch, roll] at target_frame
        
        # Return frames and target, converting target to float32 for neural network
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Python generator that yields training samples one at a time.
        
        This is a memory-efficient way to load data: instead of loading all samples
        into memory at once, it loads them on-demand as needed during training.
        
        Args:
            samples: List of sample dictionaries (from train_samples or test_samples)
            shuffle: Whether to shuffle samples each epoch (True for training, False for testing)
            
        Yields:
            Tuple of (frames, target):
            - frames: NumPy array (30, 120, 240, 3) - input sequence
            - target: NumPy array (3,) - target orientation [yaw, pitch, roll]
        """
        # Create array of indices [0, 1, 2, ..., len(samples)-1]
        indices = np.arange(len(samples))
        
        # Infinite loop: generator keeps yielding samples (for multiple epochs)
        while True:
            # Shuffle indices at the start of each epoch (if shuffle=True)
            if shuffle:
                np.random.shuffle(indices)  # Randomly reorder indices
            
            # Iterate through all samples in shuffled order
            for idx in indices:
                # Get sample dictionary at this index
                sample = samples[idx]
                try:
                    # Extract frames and target orientation for this sample
                    frames, target = self._get_sample(sample)
                    # Yield (return) this sample to the caller
                    yield frames, target
                except Exception as e:
                    # If there's an error (e.g., video file missing, frame extraction fails)
                    # Skip this problematic sample and continue with next one
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient model training.
        
        TensorFlow Datasets provide:
        - Automatic batching
        - Prefetching (load next batch while GPU processes current batch)
        - Parallel data loading
        - Memory efficiency
        
        Paper: Used for training ResNet50+GRU model with batch size 8.
        
        Args:
            split: 'train' or 'test' - which dataset to create
            shuffle: Whether to shuffle samples (True for training, False for testing)
            prefetch: Whether to prefetch batches (speeds up training by loading next batch in parallel)
            
        Returns:
            tf.data.Dataset object ready for model training
        """
        # Select appropriate sample list based on split
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Define output signature (shape and dtype) for TensorFlow
        # This tells TensorFlow what shape to expect from the generator
        output_signature = (
            # Input: frames sequence with shape (30, 120, 240, 3)
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            # Target: orientation with shape (3,) = [yaw, pitch, roll]
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create TensorFlow Dataset from Python generator
        # The generator yields samples one at a time, TensorFlow batches them automatically
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),  # Generator function
            output_signature=output_signature  # Expected output shapes
        )
        
        # Batch the dataset: group samples into batches of size batch_size
        # Example: If batch_size=8, groups 8 samples together
        # Output shape: (batch_size, 30, 120, 240, 3) for frames
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch batches for GPU efficiency
        # While GPU processes current batch, CPU loads next batch in parallel
        # AUTOTUNE = TensorFlow automatically determines optimal prefetch buffer size
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        # Return ready-to-use TensorFlow Dataset
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization.
        
        Args:
            split: 'train' or 'test'
            num_samples: Number of samples to get
            
        Returns:
            Tuple of (frames_batch, targets_batch)
        """
        samples = self.train_samples if split == 'train' else self.test_samples
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        frames_list = []
        targets_list = []
        
        for idx in selected:
            frames, target = self._get_sample(samples[idx])
            frames_list.append(frames)
            targets_list.append(target)
        
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """Clean up resources."""
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```


Creating an explanation document and finishing comments on the remaining utility methods:



Adding comments to the remaining utility methods:


```python
"""
UVPFL Data Loader - Memory Efficient Implementation

This module provides efficient data loading for the UVPFL model:
1. Loads saliency video frames on-demand (not all in memory)
2. Creates sequences of 30 frames for model input (30, 120, 240, 3)
3. Loads orientation data (Y, PI, R) as targets
4. Memory-efficient batch loading optimized for 8GB GPU

Paper Reference:
- Input shape: (30, 120, 240, 3) = (frames, height, width, channels)
- Target: (Y, PI, R) = (Yaw, Pitch, Roll) angles
"""

# Standard library imports
import os  # Operating system interface for file operations
import cv2  # OpenCV library for video frame extraction and image processing
import json  # JSON encoder/decoder for reading configuration and split files
import numpy as np  # Numerical computing library for array operations and data manipulation
import tensorflow as tf  # TensorFlow for creating TensorFlow datasets and tensor operations
from pathlib import Path  # Object-oriented filesystem paths (easier than os.path)
from typing import Dict, List, Tuple, Optional, Generator  # Type hints for function signatures and documentation
from tqdm import tqdm  # Progress bar library for showing data loading progress


# ============================================================================
# CONFIGURATION CONSTANTS (From Paper)
# ============================================================================
SEQUENCE_LENGTH = 30  # Number of frames per sequence (paper: input shape is (30, 120, 240, 3))
FRAME_HEIGHT = 120  # Height of each frame in pixels (paper specification: 120 pixels)
FRAME_WIDTH = 240  # Width of each frame in pixels (paper specification: 240 pixels)
CHANNELS = 3  # RGB color channels (3 channels: Red, Green, Blue)
PREDICTION_HORIZON = 30  # Number of frames ahead to predict (30 frames = 1 second at 30fps)


# ============================================================================
# VIDEO FRAME EXTRACTOR CLASS
# ============================================================================
class VideoFrameExtractor:
    """
    Extracts frames from saliency videos on-demand (memory efficient).
    
    Instead of loading entire videos into memory, this class extracts frames
    only when needed. This saves memory, especially important for large datasets.
    
    Paper: Uses saliency videos from 'content/saliency/' folder as input.
    """
    
    def __init__(self, saliency_path: str, target_size: Tuple[int, int] = (FRAME_WIDTH, FRAME_HEIGHT)):
        """
        Initialize the frame extractor.
        
        Args:
            saliency_path: Path to saliency videos folder (e.g., '360dataset/content/saliency')
            target_size: (width, height) tuple for resizing frames to model input size
        """
        self.saliency_path = Path(saliency_path)  # Convert to Path object for easier path operations
        self.target_size = target_size  # Target frame size: (240, 120) = (width, height)
        self._video_captures = {}  # Cache dictionary for video capture objects (not used in current implementation)
        self._video_frame_counts = {}  # Cache dictionary to store frame count for each video (avoids repeated file reads)
    
    def get_video_path(self, video_name: str) -> Path:
        """
        Get full path to saliency video file.
        
        Args:
            video_name: Name of the video (e.g., 'coaster', 'pacman')
            
        Returns:
            Path object pointing to the saliency video file
        """
        # Construct path: saliency_path/coaster_saliency.mp4
        return self.saliency_path / f'{video_name}_saliency.mp4'
    
    def get_frame_count(self, video_name: str) -> int:
        """
        Get total number of frames in a video.
        
        This method caches the frame count to avoid opening the video file
        multiple times (performance optimization).
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            
        Returns:
            Total number of frames in the video (typically ~1800 for 60-second videos at 30fps)
        """
        # Check if frame count is already cached (avoid reopening video file)
        if video_name not in self._video_frame_counts:
            # Get path to video file
            video_path = self.get_video_path(video_name)
            # Open video file using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            # Get frame count property and convert to integer
            self._video_frame_counts[video_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # Release video capture to free resources
            cap.release()
        # Return cached frame count
        return self._video_frame_counts[video_name]
    
    def extract_frame(self, video_name: str, frame_idx: int) -> np.ndarray:
        """
        Extract a single frame from the video at a specific index.
        
        Paper: Frames are extracted from saliency videos and resized to (120, 240, 3)
        for model input.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            frame_idx: Frame index (0-based, e.g., 0 = first frame, 1 = second frame)
            
        Returns:
            Frame as numpy array with shape (height, width, channels) = (120, 240, 3)
            Values normalized to [0, 1] range (for neural network training)
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        
        # Create new video capture object for each extraction (thread-safe approach)
        # This ensures each extraction is independent and doesn't interfere with others
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the desired frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        # Read the frame at that position
        # ret = True if frame was read successfully, False otherwise
        # frame = the actual frame image (BGR format)
        ret, frame = cap.read()
        # Release video capture to free resources
        cap.release()
        
        # If frame extraction failed (e.g., frame index out of bounds)
        if not ret:
            # Return a black frame (all zeros) with correct dimensions
            # Shape: (height, width, channels) = (120, 240, 3)
            return np.zeros((self.target_size[1], self.target_size[0], 3), dtype=np.float32)
        
        # Resize frame to target size (240 width, 120 height)
        # Paper: Input shape is (30, 120, 240, 3), so each frame must be 120×240
        frame = cv2.resize(frame, self.target_size)
        
        # Convert from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
        # OpenCV uses BGR by default, but neural networks expect RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values from [0, 255] to [0, 1] range
        # Neural networks train better with normalized inputs
        # Formula: normalized = original / 255.0
        frame = frame.astype(np.float32) / 255.0
        
        # Return processed frame ready for model input
        return frame
    
    def extract_sequence(self, video_name: str, start_frame: int, 
                         sequence_length: int = SEQUENCE_LENGTH) -> np.ndarray:
        """
        Extract a sequence of consecutive frames from the video.
        
        Paper: Model input requires sequences of 30 frames (SEQUENCE_LENGTH = 30)
        This method extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            start_frame: Starting frame index (0-based, e.g., 0, 15, 30, ...)
            sequence_length: Number of frames to extract (default: 30)
            
        Returns:
            Sequence as numpy array with shape (sequence_length, height, width, channels)
            Example: (30, 120, 240, 3) for 30 frames of 120×240 RGB images
        """
        # Get full path to the saliency video file
        video_path = self.get_video_path(video_name)
        # Open video file using OpenCV
        cap = cv2.VideoCapture(str(video_path))
        # Set video position to the starting frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # List to store extracted frames
        frames = []
        # Extract 'sequence_length' consecutive frames (default: 30 frames)
        for _ in range(sequence_length):
            # Read next frame from video
            # ret = True if frame read successfully, False if end of video
            # frame = the frame image (BGR format)
            ret, frame = cap.read()
            
            # If we reached end of video (no more frames available)
            if not ret:
                # Create a black frame (all zeros) with original video dimensions
                # This pads the sequence if video ends before we get 30 frames
                frame = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)
            
            # Resize frame to target size (240 width, 120 height)
            # Paper: Each frame must be 120×240 for model input
            frame = cv2.resize(frame, self.target_size)
            
            # Convert from BGR (OpenCV default) to RGB (neural network expects RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Normalize pixel values from [0, 255] to [0, 1] range
            # Formula: normalized = original / 255.0
            frame = frame.astype(np.float32) / 255.0
            
            # Add processed frame to the list
            frames.append(frame)
        
        # Release video capture to free resources
        cap.release()
        # Convert list of frames to NumPy array
        # Shape: (sequence_length, height, width, channels) = (30, 120, 240, 3)
        return np.array(frames, dtype=np.float32)
    
    def close(self):
        """
        Close all cached video capture objects and free resources.
        
        This should be called when done using the extractor to properly
        release video file handles and free memory.
        """
        # Iterate through all cached video capture objects
        for cap in self._video_captures.values():
            # Release each video capture object (closes video file handle)
            cap.release()
        # Clear the cache dictionary (remove all entries)
        self._video_captures.clear()


# ============================================================================
# UVPFL DATA LOADER CLASS (Main Data Loader)
# ============================================================================
class UVPFLDataLoader:
    """
    Main data loader for UVPFL model training and evaluation.
    
    This class provides:
    - Efficient data loading with on-demand frame extraction (saves memory)
    - Sequence creation for model input (30 frames per sequence)
    - Train/test split handling (separates users into train and test sets)
    - Batch generation with prefetching (optimizes GPU usage)
    
    Paper: Model input is sequences of 30 frames, predicting 1 second ahead (30 frames).
    """
    
    def __init__(self, 
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8):
        """
        Initialize the data loader with dataset paths and configuration.
        
        Args:
            dataset_path: Path to original 360dataset folder (contains content/ and sensory/)
            processed_path: Path to processed data folder (created by data_preprocessing.py)
            sequence_length: Number of frames per sequence (default: 30, as per paper)
            prediction_horizon: Frames ahead to predict (default: 30 = 1 second at 30fps)
            batch_size: Number of samples per batch for training (default: 8)
        """
        # Store dataset paths as Path objects for easier file operations
        self.dataset_path = Path(dataset_path)  # Path to original dataset
        self.processed_path = Path(processed_path)  # Path to preprocessed data
        
        # Store model configuration parameters
        self.sequence_length = sequence_length  # 30 frames per sequence
        self.prediction_horizon = prediction_horizon  # Predict 30 frames ahead (1 second)
        self.batch_size = batch_size  # Number of samples per batch (e.g., 8)
        
        # Initialize frame extractor for on-demand frame extraction from videos
        # This extracts frames from saliency videos only when needed (memory efficient)
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'  # Path to saliency video folder
        )
        
        # Load configuration file (contains video categories, mappings, etc.)
        self._load_config()
        
        # Load train/test split (which users are for training vs testing)
        self._load_split()
        
        # Build index of all available samples (video, user, frame combinations)
        # This creates a list of all possible training/test samples
        self._build_sample_index()
    
    def _load_config(self):
        """
        Load configuration file created by data_preprocessing.py.
        
        The config.json file contains:
        - video_categories: Mapping of categories to video lists
        - video_to_category: Reverse mapping (video name -> category)
        - all_videos: List of all video names
        - num_users: Total number of users (50)
        """
        # Path to configuration file (created during preprocessing)
        config_path = self.processed_path / 'config.json'
        # Open and read JSON configuration file
        with open(config_path, 'r') as f:
            self.config = json.load(f)  # Load entire config as dictionary
        
        # Extract configuration values for easy access
        self.video_categories = self.config['video_categories']  # e.g., {'cg_fast_paced': ['pacman', ...]}
        self.video_to_category = self.config['video_to_category']  # e.g., {'pacman': 'cg_fast_paced'}
        self.all_videos = self.config['all_videos']  # List of all 10 video names
        self.num_users = self.config['num_users']  # Total number of users (50)
    
    def _load_split(self):
        """
        Load train/test split created by data_preprocessing.py.
        
        The train_test_split.json file contains:
        - train_users: List of user IDs for training (40 users)
        - test_users: List of user IDs for testing (10 users)
        - seed: Random seed used for splitting (for reproducibility)
        """
        # Path to train/test split file (created during preprocessing)
        split_path = self.processed_path / 'train_test_split.json'
        # Open and read JSON split file
        with open(split_path, 'r') as f:
            split = json.load(f)  # Load split information as dictionary
        
        # Extract train and test user lists
        self.train_users = split['train_users']  # List of user IDs for training (e.g., [1, 2, 3, ..., 40])
        self.test_users = split['test_users']  # List of user IDs for testing (e.g., [41, 42, ..., 50])
    
    def _build_sample_index(self):
        """
        Build index of all available training and test samples.
        
        A sample represents one training example:
        - Input: 30 consecutive frames (sequence_length = 30)
        - Target: Orientation (Y, PI, R) at frame (start_frame + 30 + 30 - 1)
        
        Example:
        - start_frame = 0: Use frames 0-29 → predict frame 59 (1 second ahead)
        - start_frame = 15: Use frames 15-44 → predict frame 74 (1 second ahead)
        
        This method creates all possible samples by:
        1. Iterating through all videos and users
        2. Creating samples with stride of 15 frames (0.5 seconds) to reduce redundancy
        3. Separating samples into train/test based on user ID
        """
        # Initialize empty lists to store sample dictionaries
        self.train_samples = []  # List of training samples (dictionaries)
        self.test_samples = []  # List of test samples (dictionaries)
        
        print("Building sample index...")
        
        # Iterate through each video category (cg_fast_paced, ni_fast_paced, ni_slow_paced)
        for category, videos in self.video_categories.items():
            # Iterate through each video in this category
            for video_name in videos:
                # Get total number of frames in this video (from saliency video file)
                frame_count = self.frame_extractor.get_frame_count(video_name)
                
                # Calculate maximum starting frame index
                # We need: sequence_length (30) frames + prediction_horizon (30) frames
                # Formula: max_start = frame_count - 30 - 30 = frame_count - 60
                # Example: If video has 1800 frames, max_start = 1800 - 60 = 1740
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                # Skip this video if it's too short (can't create any samples)
                if max_start <= 0:
                    continue
                
                # Iterate through all users (1 to 50)
                for user_id in range(1, self.num_users + 1):
                    # Check if orientation data exists for this user-video pair
                    # Path: processed_data/category/video/userXX/orientation.npy
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    # Skip this user if orientation data doesn't exist
                    if not orientation_path.exists():
                        continue
                    
                    # Load orientation data to get actual frame count for this user
                    # (Some users may have fewer frames due to incomplete data)
                    orientation = np.load(orientation_path)
                    # Calculate actual maximum start frame (use minimum of video frames and user frames)
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    # Skip if can't create any samples for this user
                    if actual_max_start <= 0:
                        continue
                    
                    # Create samples with stride of 15 frames (0.5 seconds)
                    # This reduces redundancy: samples at 0, 15, 30, 45, ... instead of 0, 1, 2, 3, ...
                    # Stride of 15 means we create a sample every 0.5 seconds
                    stride = 15
                    # Iterate through possible start frames: 0, 15, 30, 45, ..., actual_max_start
                    for start_frame in range(0, actual_max_start, stride):
                        # Calculate target frame index
                        # target_frame = start_frame + sequence_length + prediction_horizon - 1
                        # Example: start_frame=0 → target_frame = 0 + 30 + 30 - 1 = 59
                        # This means: use frames 0-29 to predict frame 59 (1 second ahead)
                        target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
                        
                        # Create sample dictionary with all necessary information
                        sample = {
                            'video_name': video_name,  # e.g., 'coaster'
                            'category': category,  # e.g., 'ni_fast_paced'
                            'user_id': user_id,  # e.g., 5
                            'start_frame': start_frame,  # e.g., 0
                            'target_frame': target_frame  # e.g., 59
                        }
                        
                        # Add sample to appropriate list based on user ID
                        if user_id in self.train_users:
                            self.train_samples.append(sample)  # Add to training set
                        else:
                            self.test_samples.append(sample)  # Add to test set
        
        # Print summary of created samples
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _load_orientation(self, video_name: str, category: str, user_id: int) -> np.ndarray:
        """
        Load orientation data (Y, PI, R angles) for a specific user-video pair.
        
        Paper: Target is (Y, PI, R) = (Yaw, Pitch, Roll) angles for each frame.
        
        Args:
            video_name: Name of the video (e.g., 'coaster')
            category: Video category (e.g., 'ni_fast_paced')
            user_id: User ID (1-50)
            
        Returns:
            NumPy array with shape (num_frames, 3) containing [yaw, pitch, roll] for each frame
        """
        # Construct path to orientation file: processed_data/category/video/userXX/orientation.npy
        user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
        orientation_path = user_dir / 'orientation.npy'
        # Load NumPy array from file (created by data_preprocessing.py)
        return np.load(orientation_path)
    
    def _get_sample(self, sample: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a single training sample: extract frames and get target orientation.
        
        This is the core method that creates one training example:
        - Input: 30 consecutive frames from saliency video
        - Target: Orientation (Y, PI, R) at the prediction frame
        
        Paper: Model input is (30, 120, 240, 3) and target is (3,) = (yaw, pitch, roll)
        
        Args:
            sample: Sample dictionary containing:
                - video_name: Name of the video
                - category: Video category
                - user_id: User ID
                - start_frame: Starting frame index for sequence
                - target_frame: Frame index to predict (1 second ahead)
            
        Returns:
            Tuple of (frames_sequence, target_orientation):
            - frames_sequence: NumPy array with shape (30, 120, 240, 3) - 30 frames of 120×240 RGB images
            - target_orientation: NumPy array with shape (3,) = [yaw, pitch, roll] angles
        """
        # Extract information from sample dictionary
        video_name = sample['video_name']  # e.g., 'coaster'
        category = sample['category']  # e.g., 'ni_fast_paced'
        user_id = sample['user_id']  # e.g., 5
        start_frame = sample['start_frame']  # e.g., 0 (start of sequence)
        target_frame = sample['target_frame']  # e.g., 59 (frame to predict)
        
        # Extract sequence of 30 consecutive frames from saliency video
        # This calls VideoFrameExtractor.extract_sequence() which:
        # 1. Opens video file
        # 2. Extracts frames [start_frame, start_frame+1, ..., start_frame+29]
        # 3. Resizes each frame to 120×240
        # 4. Converts BGR to RGB
        # 5. Normalizes to [0, 1]
        # Returns: (30, 120, 240, 3) array
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        # Load orientation data for this user-video pair
        # Returns: (num_frames, 3) array with [yaw, pitch, roll] for each frame
        orientation = self._load_orientation(video_name, category, user_id)
        
        # Get target orientation at the prediction frame
        # target_frame is calculated as: start_frame + 30 + 30 - 1 = start_frame + 59
        # This gives us the orientation 1 second (30 frames) ahead
        target = orientation[target_frame]  # Extract [yaw, pitch, roll] at target_frame
        
        # Return frames and target, converting target to float32 for neural network
        return frames, target.astype(np.float32)
    
    def _data_generator(self, samples: List[Dict], shuffle: bool = True) -> Generator:
        """
        Python generator that yields training samples one at a time.
        
        This is a memory-efficient way to load data: instead of loading all samples
        into memory at once, it loads them on-demand as needed during training.
        
        Args:
            samples: List of sample dictionaries (from train_samples or test_samples)
            shuffle: Whether to shuffle samples each epoch (True for training, False for testing)
            
        Yields:
            Tuple of (frames, target):
            - frames: NumPy array (30, 120, 240, 3) - input sequence
            - target: NumPy array (3,) - target orientation [yaw, pitch, roll]
        """
        # Create array of indices [0, 1, 2, ..., len(samples)-1]
        indices = np.arange(len(samples))
        
        # Infinite loop: generator keeps yielding samples (for multiple epochs)
        while True:
            # Shuffle indices at the start of each epoch (if shuffle=True)
            if shuffle:
                np.random.shuffle(indices)  # Randomly reorder indices
            
            # Iterate through all samples in shuffled order
            for idx in indices:
                # Get sample dictionary at this index
                sample = samples[idx]
                try:
                    # Extract frames and target orientation for this sample
                    frames, target = self._get_sample(sample)
                    # Yield (return) this sample to the caller
                    yield frames, target
                except Exception as e:
                    # If there's an error (e.g., video file missing, frame extraction fails)
                    # Skip this problematic sample and continue with next one
                    continue
    
    def create_tf_dataset(self, 
                          split: str = 'train',
                          shuffle: bool = True,
                          prefetch: bool = True) -> tf.data.Dataset:
        """
        Create a TensorFlow Dataset for efficient model training.
        
        TensorFlow Datasets provide:
        - Automatic batching
        - Prefetching (load next batch while GPU processes current batch)
        - Parallel data loading
        - Memory efficiency
        
        Paper: Used for training ResNet50+GRU model with batch size 8.
        
        Args:
            split: 'train' or 'test' - which dataset to create
            shuffle: Whether to shuffle samples (True for training, False for testing)
            prefetch: Whether to prefetch batches (speeds up training by loading next batch in parallel)
            
        Returns:
            tf.data.Dataset object ready for model training
        """
        # Select appropriate sample list based on split
        samples = self.train_samples if split == 'train' else self.test_samples
        
        # Define output signature (shape and dtype) for TensorFlow
        # This tells TensorFlow what shape to expect from the generator
        output_signature = (
            # Input: frames sequence with shape (30, 120, 240, 3)
            tf.TensorSpec(shape=(self.sequence_length, FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), 
                          dtype=tf.float32),
            # Target: orientation with shape (3,) = [yaw, pitch, roll]
            tf.TensorSpec(shape=(3,), dtype=tf.float32)
        )
        
        # Create TensorFlow Dataset from Python generator
        # The generator yields samples one at a time, TensorFlow batches them automatically
        dataset = tf.data.Dataset.from_generator(
            lambda: self._data_generator(samples, shuffle),  # Generator function
            output_signature=output_signature  # Expected output shapes
        )
        
        # Batch the dataset: group samples into batches of size batch_size
        # Example: If batch_size=8, groups 8 samples together
        # Output shape: (batch_size, 30, 120, 240, 3) for frames
        dataset = dataset.batch(self.batch_size)
        
        # Prefetch batches for GPU efficiency
        # While GPU processes current batch, CPU loads next batch in parallel
        # AUTOTUNE = TensorFlow automatically determines optimal prefetch buffer size
        if prefetch:
            dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        # Return ready-to-use TensorFlow Dataset
        return dataset
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """
        Calculate number of training steps per epoch.
        
        Formula: steps_per_epoch = total_samples // batch_size
        
        Example:
        - Total train samples: 10,000
        - Batch size: 8
        - Steps per epoch: 10,000 // 8 = 1,250 steps
        
        Args:
            split: 'train' or 'test' - which dataset to calculate for
            
        Returns:
            Number of steps (batches) per epoch
        """
        # Select appropriate sample list
        samples = self.train_samples if split == 'train' else self.test_samples
        # Calculate steps: total samples divided by batch size (integer division)
        return len(samples) // self.batch_size
    
    def get_sample_batch(self, split: str = 'train', num_samples: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a small batch of samples for testing/visualization purposes.
        
        This is useful for:
        - Testing if data loading works correctly
        - Visualizing sample frames
        - Debugging model input/output
        
        Args:
            split: 'train' or 'test' - which dataset to get samples from
            num_samples: Number of samples to get (default: 4)
            
        Returns:
            Tuple of (frames_batch, targets_batch):
            - frames_batch: NumPy array (num_samples, 30, 120, 240, 3)
            - targets_batch: NumPy array (num_samples, 3) = [yaw, pitch, roll] for each sample
        """
        # Select appropriate sample list
        samples = self.train_samples if split == 'train' else self.test_samples
        # Randomly select sample indices (without replacement)
        # min() ensures we don't request more samples than available
        selected = np.random.choice(len(samples), size=min(num_samples, len(samples)), replace=False)
        
        # Lists to store extracted frames and targets
        frames_list = []
        targets_list = []
        
        # Extract each selected sample
        for idx in selected:
            # Get frames and target for this sample
            frames, target = self._get_sample(samples[idx])
            # Add to lists
            frames_list.append(frames)
            targets_list.append(target)
        
        # Convert lists to NumPy arrays
        # frames_batch shape: (num_samples, 30, 120, 240, 3)
        # targets_batch shape: (num_samples, 3)
        return np.array(frames_list), np.array(targets_list)
    
    def close(self):
        """
        Clean up resources and close video file handles.
        
        This should be called when done using the data loader to properly
        release video file handles and free memory.
        """
        # Close all video capture objects in the frame extractor
        self.frame_extractor.close()


class UVPFLDataLoaderFast:
    """
    Faster data loader that pre-loads orientation data and uses numpy arrays.
    Better for smaller datasets that fit in memory.
    """
    
    def __init__(self,
                 dataset_path: str = '360dataset',
                 processed_path: str = 'processed_data',
                 sequence_length: int = SEQUENCE_LENGTH,
                 prediction_horizon: int = PREDICTION_HORIZON,
                 batch_size: int = 8,
                 cache_frames: bool = False):
        """
        Initialize the fast data loader.
        
        Args:
            dataset_path: Path to original 360dataset
            processed_path: Path to processed data
            sequence_length: Number of frames per sequence
            prediction_horizon: Frames ahead to predict
            batch_size: Batch size for training
            cache_frames: Whether to cache extracted frames (uses more memory)
        """
        self.dataset_path = Path(dataset_path)
        self.processed_path = Path(processed_path)
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.batch_size = batch_size
        self.cache_frames = cache_frames
        
        # Initialize frame extractor
        self.frame_extractor = VideoFrameExtractor(
            self.dataset_path / 'content' / 'saliency'
        )
        
        # Frame cache
        self._frame_cache = {} if cache_frames else None
        
        # Load all configuration and data
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all configuration and orientation data."""
        # Load config
        with open(self.processed_path / 'config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load split
        with open(self.processed_path / 'train_test_split.json', 'r') as f:
            split = json.load(f)
        
        self.train_users = set(split['train_users'])
        self.test_users = set(split['test_users'])
        
        # Load all orientation data
        self.orientation_data = {}
        self.train_samples = []
        self.test_samples = []
        
        print("Loading orientation data...")
        
        for category, videos in self.config['video_categories'].items():
            for video_name in videos:
                frame_count = self.frame_extractor.get_frame_count(video_name)
                max_start = frame_count - self.sequence_length - self.prediction_horizon
                
                if max_start <= 0:
                    continue
                
                for user_id in range(1, self.config['num_users'] + 1):
                    user_dir = self.processed_path / category / video_name / f'user{user_id:02d}'
                    orientation_path = user_dir / 'orientation.npy'
                    
                    if not orientation_path.exists():
                        continue
                    
                    # Load and cache orientation
                    key = (video_name, user_id)
                    orientation = np.load(orientation_path)
                    self.orientation_data[key] = orientation
                    
                    # Create samples
                    actual_max_start = min(max_start, len(orientation) - self.sequence_length - self.prediction_horizon)
                    
                    if actual_max_start <= 0:
                        continue
                    
                    stride = 15  # 0.5 second stride
                    for start_frame in range(0, actual_max_start, stride):
                        sample = (video_name, category, user_id, start_frame)
                        
                        if user_id in self.train_users:
                            self.train_samples.append(sample)
                        else:
                            self.test_samples.append(sample)
        
        # Convert to numpy for faster indexing
        self.train_samples = np.array(self.train_samples, dtype=object)
        self.test_samples = np.array(self.test_samples, dtype=object)
        
        print(f"Loaded {len(self.orientation_data)} user-video pairs")
        print(f"Train samples: {len(self.train_samples)}")
        print(f"Test samples: {len(self.test_samples)}")
    
    def _get_frames(self, video_name: str, start_frame: int) -> np.ndarray:
        """Get frames with optional caching."""
        if self._frame_cache is not None:
            cache_key = (video_name, start_frame)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]
        
        frames = self.frame_extractor.extract_sequence(video_name, start_frame, self.sequence_length)
        
        if self._frame_cache is not None:
            self._frame_cache[cache_key] = frames
        
        return frames
    
    def _get_batch(self, samples: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Get a batch of samples."""
        batch_frames = []
        batch_targets = []
        
        for idx in indices:
            video_name, category, user_id, start_frame = samples[idx]
            user_id = int(user_id)
            start_frame = int(start_frame)
            
            # Get frames
            frames = self._get_frames(video_name, start_frame)
            
            # Get target orientation
            target_frame = start_frame + self.sequence_length + self.prediction_horizon - 1
            orientation = self.orientation_data[(video_name, user_id)]
            target = orientation[target_frame]
            
            batch_frames.append(frames)
            batch_targets.append(target)
        
        return np.array(batch_frames, dtype=np.float32), np.array(batch_targets, dtype=np.float32)
    
    def train_generator(self, shuffle: bool = True) -> Generator:
        """Generator for training data."""
        indices = np.arange(len(self.train_samples))
        
        while True:
            if shuffle:
                np.random.shuffle(indices)
            
            for i in range(0, len(indices), self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                if len(batch_indices) < self.batch_size:
                    continue  # Skip incomplete batches
                
                yield self._get_batch(self.train_samples, batch_indices)
    
    def test_generator(self) -> Generator:
        """Generator for test data."""
        indices = np.arange(len(self.test_samples))
        
        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i + self.batch_size]
            yield self._get_batch(self.test_samples, batch_indices)
    
    def get_steps_per_epoch(self, split: str = 'train') -> int:
        """Get number of steps per epoch."""
        samples = self.train_samples if split == 'train' else self.test_samples
        return len(samples) // self.batch_size


def test_data_loader():
    """Test the data loader."""
    print("=" * 60)
    print("Testing UVPFL Data Loader")
    print("=" * 60)
    
    # Initialize loader
    loader = UVPFLDataLoaderFast(
        dataset_path='360dataset',
        processed_path='processed_data',
        batch_size=4
    )
    
    # Get a sample batch
    print("\nGetting sample batch...")
    gen = loader.train_generator()
    frames, targets = next(gen)
    
    print(f"Frames shape: {frames.shape}")  # Expected: (4, 30, 120, 240, 3)
    print(f"Targets shape: {targets.shape}")  # Expected: (4, 3)
    print(f"Frames dtype: {frames.dtype}")
    print(f"Targets dtype: {targets.dtype}")
    print(f"Frames min/max: {frames.min():.3f} / {frames.max():.3f}")
    print(f"Sample target (Y, PI, R): {targets[0]}")
    
    # Test steps
    print(f"\nTrain steps per epoch: {loader.get_steps_per_epoch('train')}")
    print(f"Test steps per epoch: {loader.get_steps_per_epoch('test')}")
    
    print("\n" + "=" * 60)
    print("✅ Data loader test passed!")
    print("=" * 60)
    
    return loader


if __name__ == '__main__':
    test_data_loader()


```


Creating an explanation document:


```markdown
# Data Loader Explained - Simple Guide

## 🎯 What Does This Script Do? (In Simple Words)

**The data loader is like a smart waiter in a restaurant:**

- **You (the AI model)** sit at a table and want food (training data)
- **The waiter (data loader)** brings you food in organized batches
- Instead of bringing ALL food at once (would overflow the table!), the waiter brings it **on-demand**
- The waiter organizes the food nicely (batches, sequences) so you can eat efficiently

**In technical terms:**
- Loads video frames **only when needed** (saves memory)
- Creates sequences of 30 frames for the AI model
- Organizes data into batches for efficient training
- Handles train/test split automatically

---

## 📊 The Big Picture

```
Raw Data (Videos + Orientation)
    ↓
[Data Loader]
    ↓
Organized Batches
    ↓
AI Model Training!
```

---

## 🔢 Key Concepts Explained

### **1. What is a "Sample"?**

A **sample** is one training example:

**Input (X):**
- 30 consecutive frames from saliency video
- Shape: (30, 120, 240, 3)
- Example: Frames 0-29 from "Roller Coaster" video

**Target (Y):**
- Orientation angles at frame 59 (1 second ahead)
- Shape: (3,) = [yaw, pitch, roll]
- Example: [15.2°, -5.3°, 0.5°]

**Visual Example:**
```
Sample:
  Input:  Frames [0, 1, 2, ..., 29]  →  Predict  →  Frame 59 orientation
  (30 frames)                          (1 second)    [yaw, pitch, roll]
```

---

### **2. What is a "Sequence"?**

A **sequence** is 30 consecutive frames used as input.

**Why 30 frames?**
- Paper says: Input shape is (30, 120, 240, 3)
- 30 frames = 1 second of video (at 30fps)
- Model learns patterns from 1 second of video

**Example:**
```
Sequence starting at frame 0:
  Frame 0, Frame 1, Frame 2, ..., Frame 29
  (30 frames total)
  
Sequence starting at frame 15:
  Frame 15, Frame 16, Frame 17, ..., Frame 44
  (30 frames total)
```

---

### **3. What is "Prediction Horizon"?**

**Prediction horizon** = How far ahead we predict.

**In this code:**
- `PREDICTION_HORIZON = 30` frames
- 30 frames = 1 second (at 30fps)
- We predict **1 second ahead**

**Example:**
```
Input:  Frames 0-29 (current time)
Target: Frame 59 (1 second ahead)

Time:   0s    1s
        |     |
Frames: 0-29  30-59
        ↑     ↑
      Input  Target
```

---

### **4. What is "Stride"?**

**Stride** = How many frames we skip between samples.

**In this code:**
- `stride = 15` frames
- 15 frames = 0.5 seconds
- We create a sample every 0.5 seconds

**Why?**
- Without stride: Samples at 0, 1, 2, 3, ... (too many, redundant)
- With stride 15: Samples at 0, 15, 30, 45, ... (less redundant, faster)

**Example:**
```
Without stride (every frame):
  Sample 1: frames 0-29   → predict frame 59
  Sample 2: frames 1-30   → predict frame 60
  Sample 3: frames 2-31   → predict frame 61
  ... (very similar, redundant)

With stride 15 (every 0.5 seconds):
  Sample 1: frames 0-29   → predict frame 59
  Sample 2: frames 15-44 → predict frame 74
  Sample 3: frames 30-59 → predict frame 89
  ... (less redundant, more diverse)
```

---

## 📁 Step-by-Step: How Data Loading Works

### **Step 1: Initialize Data Loader**

```python
loader = UVPFLDataLoader(
    dataset_path='360dataset',      # Original dataset folder
    processed_path='processed_data', # Preprocessed data folder
    batch_size=8                     # 8 samples per batch
)
```

**What happens:**
1. Loads configuration (video categories, user mappings)
2. Loads train/test split (which users are train/test)
3. Builds sample index (creates list of all possible samples)

---

### **Step 2: Build Sample Index**

**The script creates all possible training samples:**

```python
For each video:
  For each user:
    For each possible start_frame (with stride 15):
      Create sample:
        - video_name: 'coaster'
        - user_id: 5
        - start_frame: 0
        - target_frame: 59  # start_frame + 30 + 30 - 1
```

**Example Calculation:**
```
Video: "Roller Coaster"
User: 5
Video has 1800 frames

Possible start frames: 0, 15, 30, 45, ..., 1740
(Stride of 15, max_start = 1800 - 30 - 30 = 1740)

Sample 1:
  start_frame = 0
  target_frame = 0 + 30 + 30 - 1 = 59
  Input: frames 0-29 → Predict: frame 59

Sample 2:
  start_frame = 15
  target_frame = 15 + 30 + 30 - 1 = 74
  Input: frames 15-44 → Predict: frame 74

... (continues for all possible start frames)
```

**Result:**
- Train samples: ~10,000+ samples
- Test samples: ~2,500+ samples

---

### **Step 3: Load a Single Sample**

**When model needs one sample:**

```python
sample = {
    'video_name': 'coaster',
    'user_id': 5,
    'start_frame': 0,
    'target_frame': 59
}

frames, target = loader._get_sample(sample)
```

**What happens:**

1. **Extract frames:**
   ```python
   # Open video file
   # Extract frames 0-29
   # Resize each to 120×240
   # Convert BGR → RGB
   # Normalize to [0, 1]
   frames = extract_sequence('coaster', 0, 30)
   # Shape: (30, 120, 240, 3)
   ```

2. **Load target:**
   ```python
   # Load orientation data
   orientation = load_orientation('coaster', 'ni_fast_paced', 5)
   # Shape: (1800, 3) - [yaw, pitch, roll] for each frame
   
   # Get target at frame 59
   target = orientation[59]
   # Shape: (3,) = [yaw, pitch, roll]
   ```

3. **Return:**
   ```python
   return frames, target
   # frames: (30, 120, 240, 3)
   # target: (3,)
   ```

---

### **Step 4: Create Batches**

**Model trains on batches (multiple samples at once):**

```python
# Create TensorFlow dataset
dataset = loader.create_tf_dataset(split='train', batch_size=8)

# Dataset automatically:
# 1. Loads samples one by one
# 2. Groups them into batches of 8
# 3. Prefetches next batch while GPU processes current batch
```

**Batch Structure:**
```
Batch of 8 samples:

Input (X):
  Shape: (8, 30, 120, 240, 3)
  - 8 samples
  - Each with 30 frames
  - Each frame is 120×240 RGB

Target (Y):
  Shape: (8, 3)
  - 8 samples
  - Each with [yaw, pitch, roll]
```

---

## 🎬 Complete Example: Loading One Batch

Let's trace through loading **one batch of 4 samples**:

### **Sample 1:**
```
video_name: 'coaster'
user_id: 5
start_frame: 0
target_frame: 59

Steps:
1. Extract frames 0-29 from coaster_saliency.mp4
2. Resize each to 120×240
3. Normalize to [0, 1]
4. Load orientation[59] = [15.2°, -5.3°, 0.5°]

Result:
  frames: (30, 120, 240, 3)
  target: [15.2, -5.3, 0.5]
```

### **Sample 2:**
```
video_name: 'coaster'
user_id: 5
start_frame: 15
target_frame: 74

Steps:
1. Extract frames 15-44 from coaster_saliency.mp4
2. Resize each to 120×240
3. Normalize to [0, 1]
4. Load orientation[74] = [16.1°, -4.8°, 0.6°]

Result:
  frames: (30, 120, 240, 3)
  target: [16.1, -4.8, 0.6]
```

### **Sample 3 & 4:**
(Same process for other samples)

### **Final Batch:**
```python
Batch Input (X):
  Shape: (4, 30, 120, 240, 3)
  [
    [30 frames from sample 1],
    [30 frames from sample 2],
    [30 frames from sample 3],
    [30 frames from sample 4]
  ]

Batch Target (Y):
  Shape: (4, 3)
  [
    [15.2, -5.3, 0.5],  # Sample 1 target
    [16.1, -4.8, 0.6],  # Sample 2 target
    [18.5, -4.2, 0.4],  # Sample 3 target
    [17.3, -5.1, 0.5]   # Sample 4 target
  ]
```

---

## 🔍 Key Formulas Used

### **Formula 1: Maximum Start Frame**

```
max_start = frame_count - sequence_length - prediction_horizon
```

**Example:**
```
Video has 1800 frames
sequence_length = 30
prediction_horizon = 30

max_start = 1800 - 30 - 30 = 1740

We can start sequences at frames: 0, 15, 30, ..., 1740
```

---

### **Formula 2: Target Frame**

```
target_frame = start_frame + sequence_length + prediction_horizon - 1
```

**Example:**
```
start_frame = 0
sequence_length = 30
prediction_horizon = 30

target_frame = 0 + 30 + 30 - 1 = 59

We use frames 0-29 to predict frame 59 (1 second ahead)
```

---

### **Formula 3: Steps Per Epoch**

```
steps_per_epoch = total_samples // batch_size
```

**Example:**
```
Total train samples: 10,000
Batch size: 8

steps_per_epoch = 10,000 // 8 = 1,250 steps

One epoch = 1,250 batches of 8 samples each
```

---

## 💡 Memory Efficiency Tricks

### **1. On-Demand Frame Extraction**

**Instead of:**
```python
# BAD: Load entire video into memory
video = load_entire_video('coaster.mp4')  # 1800 frames × 120×240×3 = HUGE!
```

**We do:**
```python
# GOOD: Extract frames only when needed
frames = extract_sequence('coaster', 0, 30)  # Only 30 frames!
```

**Memory saved:**
- Entire video: ~1800 frames × 120×240×3 × 4 bytes = ~62 MB per video
- On-demand: 30 frames × 120×240×3 × 4 bytes = ~1 MB per sample
- **60x less memory!**

---

### **2. Generator Pattern**

**Instead of:**
```python
# BAD: Load all samples into memory
all_samples = [load_sample(i) for i in range(10000)]  # HUGE memory!
```

**We do:**
```python
# GOOD: Generator yields samples one at a time
def generator():
    for sample in samples:
        yield load_sample(sample)  # Only one sample in memory at a time
```

**Memory saved:**
- All samples: 10,000 samples × ~1 MB = ~10 GB
- Generator: Only current sample = ~1 MB
- **10,000x less memory!**

---

### **3. Prefetching**

**While GPU processes current batch, CPU loads next batch in parallel:**

```
Time:
  t=0s: GPU processes batch 1, CPU loads batch 2
  t=1s: GPU processes batch 2, CPU loads batch 3
  t=2s: GPU processes batch 3, CPU loads batch 4
  ...

Result: GPU never waits for data! (Faster training)
```

---

## 🎯 Real-World Analogy

Think of it like a **Netflix streaming service**:

### **Traditional Approach (Bad):**
- Download entire movie before watching
- Takes forever, uses lots of storage

### **Data Loader Approach (Good):**
- Stream movie on-demand
- Only download what you're watching now
- Much faster, uses less storage

**Just like:**
- Traditional: Load all videos → HUGE memory
- Data Loader: Extract frames on-demand → Small memory

---

## 📈 Data Flow Summary

```
1. Initialize Loader
   ↓
2. Build Sample Index
   (Create list of all possible samples)
   ↓
3. Create TensorFlow Dataset
   (Wraps generator in TensorFlow format)
   ↓
4. Training Loop
   For each batch:
     a. Generator yields samples one by one
     b. TensorFlow groups into batches
     c. Model trains on batch
     d. Repeat
```

---

## 🚀 Key Takeaways

1. **Sample = One training example**
   - Input: 30 frames
   - Target: Orientation 1 second ahead

2. **Memory Efficient**
   - Loads frames on-demand
   - Uses generators (not all data in memory)
   - Prefetches batches in parallel

3. **Automatic Organization**
   - Handles train/test split
   - Creates batches automatically
   - Shuffles data for training

4. **Formulas:**
   - `max_start = frames - 30 - 30`
   - `target_frame = start + 30 + 30 - 1`
   - `steps = samples // batch_size`

---

## 💻 Usage Example

```python
# Initialize loader
loader = UVPFLDataLoader(
    dataset_path='360dataset',
    processed_path='processed_data',
    batch_size=8
)

# Create training dataset
train_dataset = loader.create_tf_dataset(split='train', shuffle=True)

# Train model
model.fit(
    train_dataset,
    epochs=50,
    steps_per_epoch=loader.get_steps_per_epoch('train')
)
```

**That's it!** The data loader handles everything automatically. 🎉

```


Checking for linting errors:



Added comments to `data_loader.py` and created an explanation document. Summary:

## **Summary**

### **1. Added comments to `data_loader.py`**
- Line-by-line comments explaining each function and method
- Comments explain:
  - What each class does
  - How each method works
  - Formulas and calculations
  - Memory efficiency techniques
  - Data flow and organization

### **2. Created explanation document**
- `DATA_LOADER_EXPLAINED.md` with:
  - Simple explanations
  - Step-by-step examples
  - Formulas explained
  - Real-world analogies
  - Memory efficiency tricks
  - Complete examples

---

## **Key concepts explained**

### **What is a Sample?**
- Input: 30 consecutive frames (30, 120, 240, 3)
- Target: Orientation at frame 59 (1 second ahead) = [yaw, pitch, roll]

### **How samples are created:**
```
For each video:
  For each user:
    For start_frame in [0, 15, 30, 45, ...]:
      Sample = {
        input: frames [start_frame to start_frame+29],
        target: orientation[start_frame + 59]
      }
```

### **Memory efficiency:**
1. On-demand frame extraction (only loads 30 frames at a time)
2. Generator pattern (yields samples one at a time)
3. Prefetching (loads next batch while GPU processes current batch)

---

## **Files updated**

1. `data_loader.py` — fully commented
2. `DATA_LOADER_EXPLAINED.md` — explanation guide

The lint warnings are about TensorFlow and tqdm imports not being resolved by the linter; they're in `requirements.txt` and not actual errors.

The code is now documented and explained.

```plaintext
For each video:
  For each user:
    For start_frame in [0, 15, 30, 45, ...]:
      Sample = {
        input: frames [start_frame to start_frame+29],
        target: orientation[start_frame + 59]
      }
```

