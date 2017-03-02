// Two phase matrix multiplication in Hadoop MapReduce
// Template file for homework #1 - INF 553 - Spring 2017
// - Wensheng Wu

import java.io.IOException;
import java.lang.*;

// add your import statement here if needed
// you can only import packages from java.*;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.FileSystem;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;

import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class TwoPhase {

    // mapper for processing entries of matrix A
    public static class PhaseOneMapperA
	extends Mapper<LongWritable, Text, Text, Text> {
	
	private Text outKey = new Text();
	private Text outVal = new Text();

	public void map(LongWritable key, Text value, Context context)
	    throws IOException, InterruptedException {
	    //String i,j,val;
	    
            String value1= new String();
 	    value1="A ";
	    //outKey = key;
		String arr[]=new String[3];
	    // fill in your code
	    String str = new String(value.toString());

            for(String a:str.split("\n"))
		{
			arr=a.split(",");
			value1+=""+arr[0]+" ";
			value1+=""+arr[2];
			outKey.set(arr[1]);
			outVal.set(value1);
			context.write(outKey,outVal);
		}
            //System.out.println(key);
	}

    }

    // mapper for processing entries of matrix B
    public static class PhaseOneMapperB
	extends Mapper<LongWritable, Text, Text, Text> {
	
	private Text outKey = new Text();
	private Text outVal = new Text();

	public void map(LongWritable key, Text value, Context context)
	    throws IOException, InterruptedException {
	    
	    // fill in your 
	   String value2= new String();
 	    value2="B ";
		String arr[]=new String[3];
	    // fill in your code
	    String str = new String(value.toString());
            for(String a:str.split("\n"))
		{
			arr=a.split(",");
			value2+=""+arr[1]+" ";
			value2+=""+arr[2];
			outVal.set(value2);
			outKey.set(arr[0]);
			context.write(outKey,outVal);
		}


	}
    }

    public static class PhaseOneReducer
	extends Reducer<Text, Text, Text, Text> {

	private Text outKey = new Text();
	private Text outVal = new Text();

	public void reduce(Text key, Iterable<Text> values, Context context) 
	    throws IOException, InterruptedException {
	    String val=new String();
	    // fill in your code
	    String arr[]= new String[3];
	    String k=new String();
	    int prod=1;
	    int cnt=0;
	    for(Text a : values)
		{
			
		  	val=a.toString();
			arr=val.split(" ");
			k+=arr[1]+" ";
			prod*=Integer.parseInt(arr[2]);
			cnt++;
			
		}
		outKey.set(k);
		outVal.set(Integer.toString(prod));
 	   if(cnt==2)
		{ 
			context.write(outKey,outVal);
   		}


	}

    }

    public static class PhaseTwoMapper 
	extends Mapper<Text, Text, Text, Text> {
	
	private Text outKey = new Text();
	private Text outVal = new Text();

	public void map(Text key, Text value, Context context)
	    throws IOException, InterruptedException {

	    // fill in your code
	    context.write(key,value);

	}
    }

    public static class PhaseTwoReducer 
	extends Reducer<Text, Text, Text, Text> {
	
	private Text outKey = new Text();
	private Text outVal = new Text();

	public void reduce(Text key, Iterable<Text> values, Context context)
	    throws IOException, InterruptedException {
	 
	    // fill in your code
	    int sum=0;
		int num;
	    String str=new String();
	    for(Text a:values)
	    {
	       str=a.toString();
	       num=Integer.parseInt(str);
	       sum+=num;
            }
	    outVal.set(Integer.toString(sum));
	    context.write(outKey,outVal);
	}
    }


    public static void main(String[] args) throws Exception {
	Configuration conf = new Configuration();

	Job jobOne = Job.getInstance(conf, "phase one");

	jobOne.setJarByClass(TwoPhase.class);

	jobOne.setOutputKeyClass(Text.class);
	jobOne.setOutputValueClass(Text.class);

	jobOne.setReducerClass(PhaseOneReducer.class);

	MultipleInputs.addInputPath(jobOne,
				    new Path(args[0]),
				    TextInputFormat.class,
				    PhaseOneMapperA.class);

	MultipleInputs.addInputPath(jobOne,
				    new Path(args[1]),
				    TextInputFormat.class,
				    PhaseOneMapperB.class);

	Path tempDir = new Path("temp");

	FileOutputFormat.setOutputPath(jobOne, tempDir);
	jobOne.waitForCompletion(true);


	// job two
	Job jobTwo = Job.getInstance(conf, "phase two");
	

	jobTwo.setJarByClass(TwoPhase.class);

	jobTwo.setOutputKeyClass(Text.class);
	jobTwo.setOutputValueClass(Text.class);

	jobTwo.setMapperClass(PhaseTwoMapper.class);
	jobTwo.setReducerClass(PhaseTwoReducer.class);

	jobTwo.setInputFormatClass(KeyValueTextInputFormat.class);

	FileInputFormat.setInputPaths(jobTwo, tempDir);
	FileOutputFormat.setOutputPath(jobTwo, new Path(args[2]));
	
	jobTwo.waitForCompletion(true);
	
	FileSystem.get(conf).delete(tempDir, true);
	
    }
}
