**General-Forecasting**
- 2023 11 TSMixer An All-MLP Architecture for Time Series Forecasting #ts 
	- Main Figure: 2024-02-01 ![[tsmixer.png]]
	- What did the authors try to accomplish?
		- univariate linear models can outperform deep learning
		- stacking mixer layers(MLP) for combination of same time data or seam feature data.
	- What were the key elements of the approach?
		- time mixing MLP: temporal patterns(same time)
		- feature mixing MLP: leverage covariate information
		- temporal projection: learn temporal patterns and map forecasting
		- normalisation + residual connection
	- What can you use yourself?
		- mixer: time and feature 
	- What other references do you want to follow?
		- None
- 2021 808 Autoformer Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting #transformer #ts 
	- Main Figure: 2024-02-01![[autoformer.png]]
	- Why-What?
		- Autoformer starts from how to keep temporal information in time series data without losing long-tem information. This is due to the fact that the attention based network has deeper layers. Therefore, as the data goes through layers, the temporal information will lose.
	- How(Key elements)?
		- how to extract more meaningful temporal information -> series decomposition
		- loosing the temporal information-> auto-correlation(FFT base) + skip connection
	- So what?
		- auto-correlation
		- series decomposition
	- References?
- 2019 855 N-BEATS NEURAL BASIS EXPANSION ANALYSIS FOR INTERPRETABLE TIME SERIES FORECASTING #ts 
	- Main Figure: 2024-02-01 ![[Pasted image 20240205194025.png]]
	- Why-What accomplishment?
		- improvement for univariate time series forecasting
	- How(Key elements)?
		- backward and forward residual links
		- stack of FCNN
		- 3 three different blocks - generic / trend / seasonality
	- So what?
		- backward prediction
		- trend, seasonality block
	- References?

**PV-Forecasting**
- 2019 390 A comparison of day-ahead photovoltaic power forecasting models based on T deep learning neural network #pv (CNN-LSTM)
	- Main Figure: 2024-02-01 ![[cnn_lstm_hybrid.png]]
	- What did the authors try to accomplsh?
		- comparison for CNN, LSTM, CNN-LSTM for day-ahead forecasting
	- What were the key elements of the approach?
		- directly predict power by using CNN and LSTM models
		- CLSTM(CNN+LSTM) use both weather data and power data
			- weather data -> CNN -> extracted feature
			- power data -> LSTM -> prediction
	- What can you use yourself?
		- there are experiment settings in detail. It would be useful for experiments
		- but a lack of how to use input data(preprocessing)
	- What other references do you want to follow?
		- dataset: https://dkasolarcentre.com.au/download?location=alice-springs
- 2020 106 Photovoltaic power forecasting with a hybrid deep learning approach #pv
	- Main Figure: 2024-02-07 ![[Pasted image 20240206184022.png]]
	- Why(accomplishment)?
		- stable forecasting: not use adjacent days
		- CNN: non linear feature and invariant structures
		- LSTM: temporal feature
	- What-How(Key elements)?
		- correlation for same hour -> adjacent day is important
		- CNN+LSTM
		- $P_{pred} = \alpha P_{CNN}+ \beta P_{LSTM}$ subject to $\alpha + \beta = 1$
	- So what?
		- how to use CNN+LSTM for pv power forecasting
	- References?
		- dataset: Elia. Belgium’s Electricity Transmission System Operator. Accessed: Jan. 13, 2020. [Online]. Available: https://www.elia.be/en/grid- data/power-generation/solar-pv-power-generation-data 
- 2019 173 Day-Ahead Photovoltaic Forecasting A Comparison of the Most Effective Techniques #pv 
	- Main Figure: 2024-02-11 ![[twomodels.png]]
	- Why-What?
		- forecasting depended on whether it is sunny day or cloudy day.
	- How(Key elements)?
		- case1: [[case1 model.png]]
			- irr forecasting -> avg irr -> sunny or cloudy -> power forecasting
		- case2: [[case2 model.png]]
			- weather forecast+clear sky model -> network -> power forecasting
	- So what?
		- clear sky model
		- sunny or cloudy criterian
	- References?
		- Bird, R.E.; Riordan, C. Simple Solar Spectral Model for Direct and Diffuse Irradiance on Horizontal and Tilted Planes at the Earth’s Surface for Cloudless Atmospheres. 1986.
		- Grimaccia, F.; Leva, S.; Mussetta, M.; Ogliari, E. ANN sizing procedure for the day-ahead output power forecast of a PV plant. Appl. Sci. 2017, 7, 622
- 2020 404 A day-ahead PV power forecasting method based on LSTM-RNN model and time correlation modification under partial daily pattern prediction framework.pdf #pv (RNN-LSTM + TCM + PDPP)
	- Main Figure: 2024-02-11 ![[lstm_tcm_pdpp.png]]
	- What did the authors try to accomplish?
		- previous research has an overfitting and insufficient generation
		- a lack of utilising weather changes and cloud movement
		- how to couple between weather and electricity
	- What were the key elements of the approach?
		- RNN-LSTM
		- TCM time correlation modification -> day, year correlation and weather similarity
		- PDPP partial daily pattern prediction
	- What can you use yourself?
		- way to compute the correlation 
		- classification of weather or cloud patterns
	- What other references do you want to follow?
		- None

