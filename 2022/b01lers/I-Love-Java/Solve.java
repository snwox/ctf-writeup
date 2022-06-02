import java.util.Random;
public class Solve {
    public static void main(String[] args) {
        Random random=new Random();
        random.setSeed(431289);
        int[] flag={116, 122, 54, 50, 93, 66, 98, 117, 75, 51, 97, 78, 104, 119, 90, 53, 94, 36, 105, 84, 40, 69};
        int[] iArr = {19, 17, 15, 6, 9, 4, 18, 8, 16, 13, 21, 11, 7, 0, 12, 3, 5, 2, 20, 14, 10, 1};
        int[] reverse = new int[iArr.length];
        for(int i=0;i<flag.length;i++){
            flag[i]=random.nextInt(i+1)^flag[i];
        }
        for(int i=iArr.length-1;i>=0;i--){
            reverse[iArr[i]]=flag[i];
        }
        for(int i=0;i<reverse.length/2;i++){
            flag[reverse.length-i-1]=reverse[i];
            flag[i]=reverse[reverse.length-i-1];
        }
        for(int i:flag){
            System.out.print((char)i);
        }
        
    }
}